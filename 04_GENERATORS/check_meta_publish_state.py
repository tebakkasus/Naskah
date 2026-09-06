import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent

def load_env():
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

load_env()

ig_token = os.environ["INSTAGRAM_ACCESS_TOKEN"]
ig_id = os.environ["INSTAGRAM_USER_ID"]
base = "https://graph.instagram.com/v21.0"


def get(path, params):
    query = urllib.parse.urlencode({**params, "access_token": ig_token})
    req = urllib.request.Request(f"{base}/{path}?{query}")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return {"http_status": response.status, "body": json.loads(response.read().decode("utf-8"))}
    except urllib.error.HTTPError as exc:
        return {"http_status": exc.code, "body": json.loads(exc.read().decode("utf-8"))}
    except Exception as exc:
        return {"error": type(exc).__name__, "message": str(exc)}

print("RECENT_MEDIA")
print(json.dumps(get(f"{ig_id}/media", {
    "fields": "id,caption,media_type,timestamp,permalink,children",
    "limit": "5",
}), indent=2, ensure_ascii=False))
print("PUBLISHING_LIMIT")
print(json.dumps(get(f"{ig_id}/content_publishing_limit", {
    "fields": "quota_usage,config",
}), indent=2, ensure_ascii=False))
