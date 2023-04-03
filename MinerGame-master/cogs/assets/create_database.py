import os
from aiosqlite import connect
import asyncio

path = 'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/db/mine.db'


async def create_database():
    async with connect(path) as conn:
        async with conn.cursor() as cur:
            await conn.commit()
            # テーブル名:『player』
            await cur.execute("CREATE TABLE IF NOT EXISTS player(user_id BIGINT(20), exp bigint(20))")
            await conn.commit()

            # テーブル名:『item』 カラム内容： ユーザーID 整数型, アイテムID　整数値, 個数 整数値
            await cur.execute("CREATE TABLE IF NOT EXISTS item(user_id BIGINT(20), item_id INT, count INT)")
            await conn.commit()

            # テーブル名:『ban_user』 カラム内容： ユーザーID 整数型
            await cur.execute("CREATE TABLE IF NOT EXISTS ban_user(user_id BIGINT(20))")
            await conn.commit()

            # テーブル名:『in_mine』
            await cur.execute("CREATE TABLE IF NOT EXISTS mine(user_id BIGINT(20), depth INT, place INT, player_mine INT)")
            await conn.commit()


asyncio.run(create_database())
