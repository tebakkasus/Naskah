import os
import sys
import json
import time
import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("threads")
BASE_URL = "https://graph.threads.com/v1.0"

def get_token() -> str:
    token = os.getenv("THREADS_ACCESS_TOKEN", "").strip()
    if not token:
        raise ValueError("THREADS_ACCESS_TOKEN environment variable is not set.")
    return token

@mcp.tool()
def get_my_profile() -> str:
    """Get the authenticated Threads user profile details (ID, username, profile pic, bio)."""
    token = get_token()
    url = f"{BASE_URL}/me"
    params = {
        "fields": "id,username,name,threads_profile_picture_url,threads_biography,is_verified",
        "access_token": token
    }
    resp = requests.get(url, params=params)
    return resp.text

@mcp.tool()
def list_my_posts(limit: int = 25) -> str:
    """Retrieve the most recent posts published by this Threads account."""
    token = get_token()
    url = f"{BASE_URL}/me/threads"
    params = {
        "fields": "id,media_product_type,media_type,media_url,permalink,text,timestamp,shortcode,is_quote_post,topic_tag,children{media_url,media_type}",
        "limit": limit,
        "access_token": token
    }
    resp = requests.get(url, params=params)
    return resp.text

@mcp.tool()
def post_thread(text: str, image_url: str = "", topic_tag: str = "") -> str:
    """Publish a new single thread (Text or Image).
    Args:
        text: The text content of the post (max 500 chars).
        image_url: Optional public URL of an image to attach.
        topic_tag: Optional topic tag (without # or spaces).
    """
    token = get_token()
    container_url = f"{BASE_URL}/me/threads"
    payload = {
        "access_token": token,
        "text": text
    }
    if image_url:
        payload["media_type"] = "IMAGE"
        payload["image_url"] = image_url
    else:
        payload["media_type"] = "TEXT"
        
    if topic_tag:
        payload["topic_tag"] = topic_tag.replace("#", "").strip()
        
    resp_c = requests.post(container_url, data=payload)
    if resp_c.status_code != 200:
        return f"Error creating container: {resp_c.text}"
    
    container_id = resp_c.json().get("id")
    if not container_id:
        return f"Failed to get container ID: {resp_c.text}"
    
    time.sleep(5)
    
    publish_url = f"{BASE_URL}/me/threads_publish"
    resp_p = requests.post(publish_url, data={
        "creation_id": container_id,
        "access_token": token
    })
    return resp_p.text

@mcp.tool()
def reply_to_thread(parent_post_id: str, text: str) -> str:
    """Reply to an existing thread / comment.
    Args:
        parent_post_id: ID of the thread post or reply to respond to.
        text: The text content of your reply (max 500 chars).
    """
    token = get_token()
    container_url = f"{BASE_URL}/me/threads"
    payload = {
        "access_token": token,
        "media_type": "TEXT",
        "text": text,
        "reply_to_id": parent_post_id
    }
    resp_c = requests.post(container_url, data=payload)
    if resp_c.status_code != 200:
        return f"Error creating reply container: {resp_c.text}"
    
    container_id = resp_c.json().get("id")
    time.sleep(3)
    
    publish_url = f"{BASE_URL}/me/threads_publish"
    resp_p = requests.post(publish_url, data={
        "creation_id": container_id,
        "access_token": token
    })
    return resp_p.text

@mcp.tool()
def delete_thread(media_id: str) -> str:
    """Delete a thread post owned by this account.
    Args:
        media_id: ID of the thread post to delete.
    """
    token = get_token()
    url = f"{BASE_URL}/{media_id}"
    resp = requests.delete(url, params={"access_token": token})
    return resp.text

@mcp.tool()
def get_post_insights(media_id: str) -> str:
    """Retrieve engagement metrics / insights for a specific thread post.
    Args:
        media_id: ID of the thread post.
    """
    token = get_token()
    url = f"{BASE_URL}/{media_id}/insights"
    params = {
        "metric": "views,likes,replies,reposts,quotes",
        "access_token": token
    }
    resp = requests.get(url, params=params)
    return resp.text

if __name__ == "__main__":
    mcp.run()
