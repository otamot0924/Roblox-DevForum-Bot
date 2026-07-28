from bot import send_announcement
from crawler import get_latest_announcements
from database import (
    initialize_database,
    is_announcement_sent,
    mark_announcement_as_sent,
)


def main() -> None:
    initialize_database()

    announcements = get_latest_announcements(limit=1)

    if not announcements:
        print("目前找不到公告")
        return

    # 爬蟲傳回最新到最舊，發送時反轉成最舊到最新
    for announcement in reversed(announcements):
        if is_announcement_sent(announcement["id"]):
            print(f"已發送過，跳過：{announcement['title']}")
            continue

        send_announcement(announcement)
        mark_announcement_as_sent(announcement)


if __name__ == "__main__":
    main()