"""
Naskah Social OS — Direct Meta Graph API Publisher
Supports publishing to Instagram (Single Image & Carousel) and Threads directly via Meta Graph API v21.0.

Endpoints:
- Instagram User Media: POST https://graph.instagram.com/v21.0/{ig-user-id}/media
- Instagram Media Publish: POST https://graph.instagram.com/v21.0/{ig-user-id}/media_publish
- Instagram Rate Limits: GET https://graph.instagram.com/v21.0/{ig-user-id}/content_publishing_limit
- Threads Post: POST https://graph.threads.net/v1.0/me/threads
- Threads Publish: POST https://graph.threads.net/v1.0/me/threads_publish
"""

import os
import sys
import json
import time
import pathlib
import urllib.request
import urllib.error
import urllib.parse

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent

def load_env():
    """Load environment variables from .env file if available."""
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())

load_env()

IG_BASE_URL = "https://graph.instagram.com/v21.0"
THREADS_BASE_URL = "https://graph.threads.net/v1.0"

class MetaDirectPublisher:
    def __init__(self):
        self.ig_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
        self.ig_user_id = os.environ.get("INSTAGRAM_USER_ID", "").strip()
        self.threads_token = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
        self.threads_user_id = os.environ.get("THREADS_USER_ID", "").strip()

    def check_status(self):
        """Verify tokens and print account info."""
        results = {}
        
        # Check IG
        if self.ig_token:
            url = f"{IG_BASE_URL}/me?fields=id,username,name,account_type&access_token={self.ig_token}"
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as resp:
                    ig_data = json.loads(resp.read().decode("utf-8"))
                    results["instagram"] = {
                        "status": "connected",
                        "id": ig_data.get("id"),
                        "username": ig_data.get("username"),
                        "account_type": ig_data.get("account_type")
                    }
            except Exception as e:
                results["instagram"] = {"status": "error", "error": str(e)}
        else:
            results["instagram"] = {"status": "missing_token"}

        # Check Threads
        if self.threads_token:
            url = f"{THREADS_BASE_URL}/me?fields=id,username&access_token={self.threads_token}"
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as resp:
                    th_data = json.loads(resp.read().decode("utf-8"))
                    results["threads"] = {
                        "status": "connected",
                        "id": th_data.get("id"),
                        "username": th_data.get("username")
                    }
            except Exception as e:
                results["threads"] = {"status": "error", "error": str(e)}
        else:
            results["threads"] = {"status": "missing_token"}

        return results

    def check_ig_publishing_limit(self):
        """Check Instagram publishing quota usage."""
        if not self.ig_token or not self.ig_user_id:
            return {"error": "Missing IG credentials"}
        
        url = f"{IG_BASE_URL}/{self.ig_user_id}/content_publishing_limit?fields=quota_usage,config&access_token={self.ig_token}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"error": e.read().decode("utf-8")}
        except Exception as e:
            return {"error": str(e)}

    def publish_ig_single_image(self, image_url: str, caption: str) -> dict:
        """
        Publish a single image post to Instagram.
        image_url must be a publicly accessible HTTPS URL.
        """
        if not self.ig_token or not self.ig_user_id:
            return {"error": "Missing Instagram credentials"}

        # Step 1: Create Container
        url = f"{IG_BASE_URL}/{self.ig_user_id}/media"
        payload = urllib.parse.urlencode({
            "image_url": image_url,
            "caption": caption,
            "access_token": self.ig_token
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                container_id = res.get("id")
        except urllib.error.HTTPError as e:
            return {"error": f"Failed to create media container: {e.read().decode('utf-8')}"}

        time.sleep(3)

        # Step 2: Publish Container
        pub_url = f"{IG_BASE_URL}/{self.ig_user_id}/media_publish"
        pub_payload = urllib.parse.urlencode({
            "creation_id": container_id,
            "access_token": self.ig_token
        }).encode("utf-8")

        pub_req = urllib.request.Request(pub_url, data=pub_payload, method="POST")
        try:
            with urllib.request.urlopen(pub_req) as resp:
                pub_res = json.loads(resp.read().decode("utf-8"))
                return {
                    "success": True,
                    "media_id": pub_res.get("id"),
                    "container_id": container_id
                }
        except urllib.error.HTTPError as e:
            return {"error": f"Failed to publish media: {e.read().decode('utf-8')}"}

    def publish_ig_carousel(self, image_urls: list, caption: str) -> dict:
        """
        Publish a multi-image Carousel (2-10 slides) to Instagram.
        image_urls must be a list of publicly accessible HTTPS URLs.
        """
        if not self.ig_token or not self.ig_user_id:
            return {"error": "Missing Instagram credentials"}

        if len(image_urls) < 2 or len(image_urls) > 10:
            return {"error": f"Carousel requires between 2 and 10 images. Given: {len(image_urls)}"}

        # Step 1: Create item containers for each slide
        item_container_ids = []
        for idx, img_url in enumerate(image_urls):
            url = f"{IG_BASE_URL}/{self.ig_user_id}/media"
            payload = urllib.parse.urlencode({
                "image_url": img_url,
                "is_carousel_item": "true",
                "access_token": self.ig_token
            }).encode("utf-8")

            req = urllib.request.Request(url, data=payload, method="POST")
            try:
                with urllib.request.urlopen(req) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    item_id = res.get("id")
                    if not item_id:
                        return {"error": f"No container ID returned for slide {idx+1}"}
                    item_container_ids.append(item_id)
            except urllib.error.HTTPError as e:
                return {"error": f"Failed creating container for slide {idx+1}: {e.read().decode('utf-8')}"}
            
            time.sleep(1)

        # Step 2: Create the parent Carousel Container
        carousel_url = f"{IG_BASE_URL}/{self.ig_user_id}/media"
        carousel_payload = urllib.parse.urlencode({
            "media_type": "CAROUSEL",
            "children": ",".join(item_container_ids),
            "caption": caption,
            "access_token": self.ig_token
        }).encode("utf-8")

        req_car = urllib.request.Request(carousel_url, data=carousel_payload, method="POST")
        try:
            with urllib.request.urlopen(req_car) as resp:
                car_res = json.loads(resp.read().decode("utf-8"))
                carousel_container_id = car_res.get("id")
        except urllib.error.HTTPError as e:
            return {"error": f"Failed creating carousel container: {e.read().decode('utf-8')}"}

        time.sleep(5)

        # Step 3: Publish the Carousel
        pub_url = f"{IG_BASE_URL}/{self.ig_user_id}/media_publish"
        pub_payload = urllib.parse.urlencode({
            "creation_id": carousel_container_id,
            "access_token": self.ig_token
        }).encode("utf-8")

        req_pub = urllib.request.Request(pub_url, data=pub_payload, method="POST")
        try:
            with urllib.request.urlopen(req_pub) as resp:
                publish_res = json.loads(resp.read().decode("utf-8"))
                return {
                    "success": True,
                    "media_id": publish_res.get("id"),
                    "carousel_container_id": carousel_container_id,
                    "item_containers": item_container_ids,
                    "total_slides": len(image_urls)
                }
        except urllib.error.HTTPError as e:
            return {"error": f"Failed publishing carousel: {e.read().decode('utf-8')}"}

    def publish_thread(self, text: str, image_url: str = "", topic_tag: str = "") -> dict:
        """Publish a thread post directly via Meta Threads API."""
        if not self.threads_token:
            return {"error": "Missing Threads credentials"}

        url = f"{THREADS_BASE_URL}/me/threads"
        data = {
            "access_token": self.threads_token,
            "text": text
        }
        if image_url:
            data["media_type"] = "IMAGE"
            data["image_url"] = image_url
        else:
            data["media_type"] = "TEXT"

        if topic_tag:
            data["topic_tag"] = topic_tag.replace("#", "").strip()

        payload = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(url, data=payload, method="POST")

        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                container_id = res.get("id")
        except urllib.error.HTTPError as e:
            return {"error": f"Failed to create thread container: {e.read().decode('utf-8')}"}

        time.sleep(4)

        pub_url = f"{THREADS_BASE_URL}/me/threads_publish"
        pub_payload = urllib.parse.urlencode({
            "creation_id": container_id,
            "access_token": self.threads_token
        }).encode("utf-8")

        req_pub = urllib.request.Request(pub_url, data=pub_payload, method="POST")
        try:
            with urllib.request.urlopen(req_pub) as resp:
                pub_res = json.loads(resp.read().decode("utf-8"))
                return {
                    "success": True,
                    "thread_id": pub_res.get("id"),
                    "container_id": container_id
                }
        except urllib.error.HTTPError as e:
            return {"error": f"Failed to publish thread: {e.read().decode('utf-8')}"}

if __name__ == "__main__":
    publisher = MetaDirectPublisher()
    status = publisher.check_status()
    print("=== Meta Direct API Connection Status ===")
    print(json.dumps(status, indent=2))
    
    limits = publisher.check_ig_publishing_limit()
    print("\n=== Instagram Content Publishing Quota ===")
    print(json.dumps(limits, indent=2))
