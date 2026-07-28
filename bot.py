import os

import httpx
from dotenv import load_dotenv


load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_announcement(announcement: dict) -> None:
    if not DISCORD_WEBHOOK_URL:
        raise RuntimeError("找不到 DISCORD_WEBHOOK_URL")

    tags = announcement.get("tags", [])
    tags_text = ", ".join(tags) if tags else "無"

    payload = {
        "username": "Roblox DevForum 官方通知",
        "embeds": [
            {
                "title": announcement["title"],
                "url": announcement["url"],
                "description": "Roblox Developer Forum 發布了新的官方公告。",
                "color": 5793266,
                "fields": [
                    {
                        "name": "標籤",
                        "value": tags_text,
                        "inline": True,
                    },
                    {
                        "name": "瀏覽次數",
                        "value": str(announcement["views"]),
                        "inline": True,
                    },
                ],
                "footer": {
                    "text": "來源：Roblox Developer Forum"
                },
                "timestamp": announcement["created_at"],
            }
        ],
    }

    response = httpx.post(
        DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=15,
    )
    response.raise_for_status()

    print(f"已發送 Discord 通知：{announcement['title']}")


if __name__ == "__main__":
    print("請透過 main.py 執行通知流程")