from typing import Dict, List, Union
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from string import ascii_lowercase


mongo = MongoCli(MONGO_URL).Rankings

warnsdb = mongo.warns



async def int_to_alpha(user_id : int) -> str:
    alphabet = list(ascii_lowercase)[:10]
    user_id = str(user_id)
    return "".join(alphabet[int(i)] for i in user_id)        

async def get_warns(chat_id : int) -> Dict[str,int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    return {} if not warns else warns["warns"]


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


    

async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn
    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )
    await warnsdb.update_one({"chat_id": chat_id}, {"$set": {"mode": "BAN"}})
    
    


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"warns": warnsd}},
            upsert=True,
        )
        return True
    return False


async def get_warns_count() -> dict:
    chats_count = 0
    warns_count = 0
    async for chat in warnsdb.find({"chat_id": {"$lt": 0}}):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}
