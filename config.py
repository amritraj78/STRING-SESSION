from os import getenv
from dotenv import load_dotenv

load_dotenv()


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
