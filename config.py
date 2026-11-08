import time
from os import getenv
from dotenv import load_dotenv

load_dotenv()

START_TIME = time.time()


def get_readable_time(seconds: int) -> str:
    count = int(seconds)
    days, count = divmod(count, 86400)
    hours, count = divmod(count, 3600)
    minutes, seconds = divmod(count, 60)
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


def get_int(key: str, default: int = 0) -> int:
    val = getenv(key)
    if val:
        try:
            return int(val.strip())
        except (ValueError, TypeError):
            pass
    return default


API_ID = get_int("API_ID")
API_HASH = getenv("API_HASH", "")

BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = get_int("OWNER_ID")

MONGO_DB_URI = getenv("MONGO_DB_URI") or getenv("MONGO_URL") or None
MUST_JOIN = getenv("MUST_JOIN", "amrit_feel privatethink")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "amrit_feel")
CHANNEL = getenv("CHANNEL", "privatethink")
PORT = get_int("PORT", 8000)
