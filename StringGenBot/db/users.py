from StringGenBot.db import db

usersdb = db.users

# In-memory cache to eliminate redundant MongoDB network queries
_SERVED_CACHE = set()


async def is_served_user(user_id: int) -> bool:
    if user_id in _SERVED_CACHE:
        return True
    try:
        user = await usersdb.find_one({"user_id": user_id})
        if user:
            _SERVED_CACHE.add(user_id)
            return True
        return False
    except Exception:
        return False


async def get_served_users() -> list:
    users_list = []
    try:
        async for user in usersdb.find({"user_id": {"$gt": 0}}):
            users_list.append(user)
            uid = user.get("user_id")
            if uid:
                _SERVED_CACHE.add(uid)
    except Exception:
        pass
    return users_list


async def add_served_user(user_id: int):
    if user_id in _SERVED_CACHE:
        return
    try:
        is_served = await is_served_user(user_id)
        if is_served:
            return
        await usersdb.insert_one({"user_id": user_id})
        _SERVED_CACHE.add(user_id)
    except Exception:
        return None
