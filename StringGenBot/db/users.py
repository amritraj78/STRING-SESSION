from StringGenBot.db import db

usersdb = db.users


async def is_served_user(user_id: int) -> bool:
    try:
        user = await usersdb.find_one({"user_id": user_id})
        return bool(user)
    except Exception:
        return False


async def get_served_users() -> list:
    users_list = []
    try:
        async for user in usersdb.find({"user_id": {"$gt": 0}}):
            users_list.append(user)
    except Exception:
        pass
    return users_list


async def add_served_user(user_id: int):
    try:
        is_served = await is_served_user(user_id)
        if is_served:
            return
        return await usersdb.insert_one({"user_id": user_id})
    except Exception:
        return None
