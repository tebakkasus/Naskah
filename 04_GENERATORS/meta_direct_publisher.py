"""
Naskah Social OS — Direct Meta Graph API Publisher

Direct integration with official Meta APIs (no Composio):
- Instagram Content Publishing API for single-image and carousel posts
- Threads Publishing API for companion text/image posts

Important Instagram publishing constraint:
Meta fetches each media URL from its own servers. Image URLs must be public HTTPS
URLs and image feed publishing is safest with JPEG files.
"""

from __future__ import annotations

import json
import os
import pathlib
import time
from typing import Any

import requests

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
IG_BASE_URL = "https://graph.instagram.com/v21.0"
THREADS_BASE_URL = "https://graph.threads.net/v1.0"
DEFAULT_TIMEOUT = 60


def load_env() -> None:
    """Load environment variables from the project .env file if available."""
    env_file = ROOT_DIR / ".env"
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_env()


class MetaApiError(RuntimeError):
    """Raised when Meta returns a non-success response."""


class MetaDirectPublisher:
    def __init__(self) -> None:
        self.ig_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
        self.ig_user_id = os.environ.get("INSTAGRAM_USER_ID", "").strip()
        self.threads_token = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
        self.threads_user_id = os.environ.get("THREADS_USER_ID", "").strip()
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NaskahSocialOS/1.0"})

    def _request_json(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            response = self.session.request(
                method,
                url,
                params=params,
                data=data,
                timeout=DEFAULT_TIMEOUT,
            )
        except requests.RequestException as exc:
            return {
                "success": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
            }

        try:
            payload = response.json()
        except ValueError:
            payload = {"raw": response.text}

        if not response.ok:
            return {
                "success": False,
                "http_status": response.status_code,
                "error": payload,
            }

        if isinstance(payload, dict):
            payload.setdefault("success", True)
            payload.setdefault("http_status", response.status_code)
            return payload
        return {"success": True, "http_status": response.status_code, "data": payload}

    def _ig_get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        merged = {**(params or {}), "access_token": self.ig_token}
        return self._request_json("GET", f"{IG_BASE_URL}/{path}", params=merged)

    def _ig_post(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        merged = {**data, "access_token": self.ig_token}
        return self._request_json("POST", f"{IG_BASE_URL}/{path}", data=merged)

    def _threads_get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        merged = {**(params or {}), "access_token": self.threads_token}
        return self._request_json("GET", f"{THREADS_BASE_URL}/{path}", params=merged)

    def _threads_post(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        merged = {**data, "access_token": self.threads_token}
        return self._request_json("POST", f"{THREADS_BASE_URL}/{path}", data=merged)

    def check_status(self) -> dict[str, Any]:
        """Verify Instagram and Threads credentials through read-only calls."""
        results: dict[str, Any] = {}

        if self.ig_token:
            ig_data = self._ig_get("me", {"fields": "id,username,name,account_type"})
            if ig_data.get("success"):
                results["instagram"] = {
                    "status": "connected",
                    "id": ig_data.get("id"),
                    "username": ig_data.get("username"),
                    "account_type": ig_data.get("account_type"),
                }
            else:
                results["instagram"] = {"status": "error", "details": ig_data}
        else:
            results["instagram"] = {"status": "missing_token"}

        if self.threads_token:
            threads_data = self._threads_get("me", {"fields": "id,username"})
            if threads_data.get("success"):
                results["threads"] = {
                    "status": "connected",
                    "id": threads_data.get("id"),
                    "username": threads_data.get("username"),
                }
            else:
                results["threads"] = {"status": "error", "details": threads_data}
        else:
            results["threads"] = {"status": "missing_token"}

        return results

    def check_ig_publishing_limit(self) -> dict[str, Any]:
        """Check Instagram publishing quota usage."""
        if not self.ig_token or not self.ig_user_id:
            return {"success": False, "error": "Missing IG credentials"}
        return self._ig_get(
            f"{self.ig_user_id}/content_publishing_limit",
            {"fields": "quota_usage,config"},
        )

    def list_recent_ig_media(self, limit: int = 10) -> dict[str, Any]:
        """List recent Instagram media for duplicate checks and verification."""
        if not self.ig_token or not self.ig_user_id:
            return {"success": False, "error": "Missing IG credentials"}
        return self._ig_get(
            f"{self.ig_user_id}/media",
            {
                "fields": "id,caption,media_type,timestamp,permalink,children",
                "limit": str(limit),
            },
        )

    def get_ig_media(self, media_id: str) -> dict[str, Any]:
        """Read one Instagram media object after publishing."""
        if not self.ig_token:
            return {"success": False, "error": "Missing IG credentials"}
        return self._ig_get(
            media_id,
            {"fields": "id,caption,media_type,timestamp,permalink,children"},
        )

    def check_ig_container_status(self, container_id: str) -> dict[str, Any]:
        """Check a media container's publishing readiness/status."""
        if not self.ig_token:
            return {"success": False, "error": "Missing IG credentials"}
        return self._ig_get(container_id, {"fields": "status_code"})

    def wait_for_ig_container(
        self,
        container_id: str,
        *,
        max_attempts: int = 6,
        delay_seconds: int = 5,
    ) -> dict[str, Any]:
        """Wait until an Instagram container is ready enough to publish."""
        last_status: dict[str, Any] = {}
        for _ in range(max_attempts):
            last_status = self.check_ig_container_status(container_id)
            status_code = last_status.get("status_code")
            if status_code in {"FINISHED", "PUBLISHED"}:
                return last_status
            if status_code in {"ERROR", "EXPIRED"}:
                return last_status
            time.sleep(delay_seconds)
        return last_status

    @staticmethod
    def _validate_public_https_urls(image_urls: list[str]) -> dict[str, Any] | None:
        bad_urls = [url for url in image_urls if not url.startswith("https://")]
        if bad_urls:
            return {"success": False, "error": "All image URLs must be public HTTPS URLs", "bad_urls": bad_urls}
        return None

    def publish_ig_single_image(self, image_url: str, caption: str) -> dict[str, Any]:
        """Publish a single image post to Instagram."""
        if not self.ig_token or not self.ig_user_id:
            return {"success": False, "error": "Missing Instagram credentials"}

        validation_error = self._validate_public_https_urls([image_url])
        if validation_error:
            return validation_error

        container = self._ig_post(
            f"{self.ig_user_id}/media",
            {"image_url": image_url, "caption": caption},
        )
        if not container.get("success"):
            return {"success": False, "stage": "create_media_container", "details": container}

        container_id = container.get("id")
        if not container_id:
            return {"success": False, "stage": "create_media_container", "details": container}

        self.wait_for_ig_container(container_id)
        publish_result = self._ig_post(
            f"{self.ig_user_id}/media_publish",
            {"creation_id": container_id},
        )
        if not publish_result.get("success"):
            return {
                "success": False,
                "stage": "media_publish",
                "container_id": container_id,
                "details": publish_result,
            }

        media_id = publish_result.get("id")
        return {
            "success": True,
            "media_id": media_id,
            "container_id": container_id,
            "media": self.get_ig_media(media_id) if media_id else None,
        }

    def publish_ig_carousel(self, image_urls: list[str], caption: str) -> dict[str, Any]:
        """Publish a multi-image Instagram carousel (2-10 images)."""
        if not self.ig_token or not self.ig_user_id:
            return {"success": False, "error": "Missing Instagram credentials"}
        if len(image_urls) < 2 or len(image_urls) > 10:
            return {"success": False, "error": f"Carousel requires between 2 and 10 images. Given: {len(image_urls)}"}

        validation_error = self._validate_public_https_urls(image_urls)
        if validation_error:
            return validation_error

        item_container_ids: list[str] = []
        for idx, image_url in enumerate(image_urls, start=1):
            item = self._ig_post(
                f"{self.ig_user_id}/media",
                {
                    "image_url": image_url,
                    "is_carousel_item": "true",
                },
            )
            if not item.get("success") or not item.get("id"):
                return {
                    "success": False,
                    "stage": "create_carousel_item",
                    "slide": idx,
                    "created_item_containers": item_container_ids,
                    "details": item,
                }
            item_container_ids.append(item["id"])
            item_status = self.wait_for_ig_container(item["id"], max_attempts=6, delay_seconds=5)
            if item_status.get("status_code") in {"ERROR", "EXPIRED"}:
                return {
                    "success": False,
                    "stage": "carousel_item_status",
                    "slide": idx,
                    "item_containers": item_container_ids,
                    "details": item_status,
                }
            time.sleep(1)

        carousel = self._ig_post(
            f"{self.ig_user_id}/media",
            {
                "media_type": "CAROUSEL",
                "children": ",".join(item_container_ids),
                "caption": caption,
            },
        )
        if not carousel.get("success") or not carousel.get("id"):
            return {
                "success": False,
                "stage": "create_carousel_container",
                "item_containers": item_container_ids,
                "details": carousel,
            }

        carousel_container_id = carousel["id"]
        container_status = self.wait_for_ig_container(carousel_container_id)
        if container_status.get("status_code") in {"ERROR", "EXPIRED"}:
            return {
                "success": False,
                "stage": "carousel_container_status",
                "carousel_container_id": carousel_container_id,
                "item_containers": item_container_ids,
                "details": container_status,
            }

        publish_result = self._ig_post(
            f"{self.ig_user_id}/media_publish",
            {"creation_id": carousel_container_id},
        )
        if not publish_result.get("success"):
            return {
                "success": False,
                "stage": "media_publish",
                "carousel_container_id": carousel_container_id,
                "item_containers": item_container_ids,
                "details": publish_result,
            }

        media_id = publish_result.get("id")
        return {
            "success": True,
            "media_id": media_id,
            "carousel_container_id": carousel_container_id,
            "item_containers": item_container_ids,
            "total_slides": len(image_urls),
            "media": self.get_ig_media(media_id) if media_id else None,
        }

    def publish_thread(self, text: str, image_url: str = "", topic_tag: str = "") -> dict[str, Any]:
        """Publish a Threads post directly via the official Threads API."""
        if not self.threads_token:
            return {"success": False, "error": "Missing Threads credentials"}

        data: dict[str, Any] = {"text": text, "media_type": "TEXT"}
        if image_url:
            validation_error = self._validate_public_https_urls([image_url])
            if validation_error:
                return validation_error
            data.update({"media_type": "IMAGE", "image_url": image_url})
        if topic_tag:
            data["topic_tag"] = topic_tag.replace("#", "").strip()

        container = self._threads_post("me/threads", data)
        if not container.get("success") or not container.get("id"):
            return {"success": False, "stage": "create_thread_container", "details": container}

        container_id = container["id"]
        time.sleep(4)
        publish_result = self._threads_post("me/threads_publish", {"creation_id": container_id})
        if not publish_result.get("success"):
            return {
                "success": False,
                "stage": "threads_publish",
                "container_id": container_id,
                "details": publish_result,
            }

        return {
            "success": True,
            "thread_id": publish_result.get("id"),
            "container_id": container_id,
        }


def main() -> None:
    publisher = MetaDirectPublisher()
    print("=== Meta Direct API Connection Status ===")
    print(json.dumps(publisher.check_status(), indent=2))
    print("\n=== Instagram Content Publishing Quota ===")
    print(json.dumps(publisher.check_ig_publishing_limit(), indent=2))


if __name__ == "__main__":
    main()
