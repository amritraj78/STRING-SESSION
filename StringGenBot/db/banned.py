from StringGenBot.db import db

banned_db = db.banned

_BANNED_CACHE = set()
_CACHE_INITIALIZED = False


async def is_banned_user(user_id: int) -> bool:
    global _CACHE_INITIALIZED
    if user_id in _BANNED_CACHE:
        return True
    try:
        if not _CACHE_INITIALIZED:
            async for u in banned_db.find({"user_id": {"$gt": 0}}):
                uid = u.get("user_id")
                if uid:
                    _BANNED_CACHE.add(uid)
            _CACHE_INITIALIZED = True
            if user_id in _BANNED_CACHE:
                return True
        user = await banned_db.find_one({"user_id": user_id})
        if user:
            _BANNED_CACHE.add(user_id)
            return True
        return False
    except Exception:
        return False


async def add_banned_user(user_id: int) -> bool:
    try:
        if await is_banned_user(user_id):
            return True
        await banned_db.insert_one({"user_id": user_id})
        _BANNED_CACHE.add(user_id)
        return True
    except Exception:
        _BANNED_CACHE.add(user_id)
        return True


async def remove_banned_user(user_id: int) -> bool:
    try:
        await banned_db.delete_one({"user_id": user_id})
        _BANNED_CACHE.discard(user_id)
        return True
    except Exception:
        _BANNED_CACHE.discard(user_id)
        return True


async def get_banned_users() -> list:
    banned_list = []
    try:
        async for u in banned_db.find({"user_id": {"$gt": 0}}):
            uid = u.get("user_id")
            if uid:
                banned_list.append(uid)
                _BANNED_CACHE.add(uid)
    except Exception:
        return list(_BANNED_CACHE)
    return banned_list
