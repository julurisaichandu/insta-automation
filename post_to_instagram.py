import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

IG_USER_ID = os.environ["IG_USER_ID"]
ACCESS_TOKEN = os.environ["IG_ACCESS_TOKEN"]
API_VERSION = "v25.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"


def create_image_container(image_url, caption=""):
    resp = requests.post(
        f"{BASE_URL}/{IG_USER_ID}/media",
        data={"image_url": image_url, "caption": caption, "access_token": ACCESS_TOKEN},
    )
    if not resp.ok:
        raise RuntimeError(f"Container creation failed: {resp.status_code} {resp.text}")
    return resp.json()["id"]


def publish_container(creation_id):
    resp = requests.post(
        f"{BASE_URL}/{IG_USER_ID}/media_publish",
        data={"creation_id": creation_id, "access_token": ACCESS_TOKEN},
    )
    if not resp.ok:
        raise RuntimeError(f"Publish failed: {resp.status_code} {resp.text}")
    return resp.json()


def post_image(image_url, caption=""):
    creation_id = create_image_container(image_url, caption)
    return publish_container(creation_id)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python post_to_instagram.py <public_image_url> [caption]")
        raise SystemExit(1)
    image_url = sys.argv[1]
    caption = sys.argv[2] if len(sys.argv) > 2 else ""
    result = post_image(image_url, caption)
    print("Published:", result)
