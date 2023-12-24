from typing import Dict, List, Union
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli


mongo = MongoCli(MONGO_URL).Rankings



afkdb = mongo.afk


async def is_afk(user_id: int) -> bool:
    user = await afkdb.find_one({"user_id": user_id})
    return (False, {}) if not user else (True, user["reason"])


async def add_afk(user_id: int, mode):
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
    )


async def remove_afk(user_id: int):
    user = await afkdb.find_one({"user_id": user_id})
    if user:
        return await afkdb.delete_one({"user_id": user_id})


async def get_afk_users() -> list:
    users = afkdb.find({"user_id": {"$gt": 0}})
    return [] if not users else list(await users.to_list(length=1000000000))


