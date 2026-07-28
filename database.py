import sqlite3 #SQLite資料庫
from datetime import datetime, timezone
from pathlib import Path #處理檔案路徑


DATABASE_PATH = Path(__file__).parent / "notifications.db"

#資料庫連線
def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_PATH)

#初始化不回傳資料
def initialize_database() -> None:
    with get_connection() as connection:
        #建立資料表，如果不存在的話
        #ID當主鍵
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sent_announcements (
                topic_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                sent_at TEXT NOT NULL
            )
            """
        )

#檢查公告是否已發送過
def is_announcement_sent(topic_id: int) -> bool:
    with get_connection() as connection:
        #檢查資料表中是否存在該公告的ID
        result = connection.execute(
            """
            SELECT 1
            FROM sent_announcements
            WHERE topic_id = ?
            """,
            (topic_id,),
        ).fetchone() #取得第一筆結果

    return result is not None

#將公告標記為已發送
def mark_announcement_as_sent(announcement: dict) -> None:
    sent_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO sent_announcements (
                topic_id,
                title,
                url,
                sent_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                announcement["id"],
                announcement["title"],
                announcement["url"],
                sent_at,
            ),
        )