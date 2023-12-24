from typing import Dict, List, Union
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL).Rankings

coupledb = mongo.couples

   
async def _get_lovers(cid: int):
    lovers = await coupledb.find_one({"chat_id": cid})
    lovers = lovers["couple"] if lovers else {}
    return lovers

async def _get_image(cid: int):
    lovers = await coupledb.find_one({"chat_id": cid})
    lovers = lovers["img"] if lovers else {}
    return lovers

async def get_couple(cid: int, date: str):
    lovers = await _get_lovers(cid)
    return lovers[date] if date in lovers else False


async def save_couple(cid: int, date: str, couple: dict, img: str):
    lovers = await _get_lovers(cid)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": cid},
        {"$set": {"couple": lovers, "img": img}},
        upsert=True,
    )

