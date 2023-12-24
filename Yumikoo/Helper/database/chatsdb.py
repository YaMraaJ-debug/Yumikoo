from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient


mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.chats



async def get_served_chats():
    chat_list = []
    async for chat in db.chats.find({"chat": {"$lt": 0}}):
        chat_list.append(chat['chat'])
    return chat_list

async def is_served_chat(chat):
    chats = await get_served_chats()
    return chat in chats

async def add_served_chat(chat):
    chats = await get_served_chats()
    if chat in chats:
        return
    else:
        await db.chats.insert_one({"chat": chat})

async def remove_served_chat(chat):
    chats = await get_served_chats()
    if chat not in chats:
        return
    else:
        await db.chats.delete_one({"chat": chat})
