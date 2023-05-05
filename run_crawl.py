from typing import List
from dotenv import load_dotenv
from src.crawling.crawl import Crawl
from src.database.database import Database
import os

if __name__ == "__main__":
    load_dotenv()
    db = Database()
    db.create_tables()

    status = str(os.getenv("CRAWLER_STATUS"))
    start_urls: List[str] = str(os.getenv("CRAWLER_START_URLS")).split()
    max_threads = str(os.getenv("CRAWLER_MAX_THREADS"))
    crawler_duration_sec = int(str(os.getenv("CRAWLER_DURATION_SECONDS")))
    try:
        msb_keyword = str(os.getenv("CRAWLER_KEYWORD"))
    except:
        msb_keyword = ""

    if msb_keyword != "":
        bfs_duration_sec = crawler_duration_sec // 2
        msb_duration_sec = crawler_duration_sec // 2
    else:
        bfs_duration_sec = crawler_duration_sec
        msb_duration_sec = 0

    c = Crawl(status, start_urls, max_threads, bfs_duration_sec,
              msb_duration_sec, msb_keyword)
    c.run()
