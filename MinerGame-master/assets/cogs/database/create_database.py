import os
from aiosqlite import connect
import asyncio

IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_PATH = f'{IMG_PATH}/background.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'


async def create_database():
    async with connect(DB_PATH) as conn:
        async with conn.cursor() as cur:
            await conn.commit()
            # テーブル名:『player』カラム名: ユーザーID 整数値, exp 整数値
            await cur.execute("CREATE TABLE IF NOT EXISTS player(user_id BIGINT(20), exp INT)")
            await conn.commit()

            # テーブル名:『position』カラム名: ユーザーID 整数値, x 整数値, y 整数値, 階層 整数値
            await cur.execute("CREATE TABLE IF NOT EXISTS position(user_id BIGINT(20), x INT, y INT, layer INT)")
            await conn.commit()

            # テーブル名:『item』 カラム内容： ユーザーID 整数型, アイテムID　整数値, 個数 整数値
            await cur.execute("CREATE TABLE IF NOT EXISTS item(user_id BIGINT(20), item_id INT, count INT)")
            await conn.commit()

            # テーブル名:『ban_user』 カラム内容： ユーザーID 整数型
            await cur.execute("CREATE TABLE IF NOT EXISTS ban_user(user_id BIGINT(20))")
            await conn.commit()

            # テーブル名:『mine』カラム内容: ユーザーID 整数値, x 整数値, y 整数値, 堀った数 整数値
            await cur.execute("CREATE TABLE IF NOT EXISTS mine(user_id BIGINT(20), x INT, y INT, count INT)")
            await conn.commit()


asyncio.run(create_database())
