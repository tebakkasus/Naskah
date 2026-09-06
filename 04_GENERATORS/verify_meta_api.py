"""
Script utility untuk verifikasi koneksi Meta Graph API (Instagram & Threads).
Memeriksa token, ID akun, dan permission.
"""

import os
import sys
import json
import urllib.request
import urllib.error

GRAPH_API_VERSION = "v20.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def check_token(access_token: str):
    url = f"{BASE_URL}/me?fields=id,name&access_token={access_token}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("✓ Token valid!")
            print(f"  User/Page ID: {data.get('id')}")
            print(f"  Name: {data.get('name')}")
            return data
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        print(f"✗ HTTP Error {e.code}: {err_body}")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

if __name__ == "__main__":
    token = os.environ.get("META_ACCESS_TOKEN", "").strip()
    if not token and len(sys.argv) > 1:
        token = sys.argv[1].strip()
    
    if not token:
        print("Usage: python verify_meta_api.py <ACCESS_TOKEN>")
        print("Atau set environment variable META_ACCESS_TOKEN.")
        sys.exit(1)
        
    check_token(token)
