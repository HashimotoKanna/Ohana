import os
from aiosqlite import connect
import asyncio
ABS_PATH =  "/home/souryo1010/discordbot/Ohana/"
IMG_PATH = ABS_PATH + "assets/img"
DB_PATH = ABS_PATH + "assets/db/mine.db"
BG_PATH = f'{IMG_PATH}/background.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'


async def create_database():
    async with connect(DB_PATH) as conn:
        async with conn.cursor() as cur:
            await conn.commit()
            # テーブル名:『player』カラム名: ユーザーID 整数値, exp 整数値, 堀った数 整数値
            await cur.execute("CREATE TABLE IF NOT EXISTS player(user_id BIGINT(20), exp INT, mine_count INT)")
            await conn.commit()

            # テーブル名:『position』カラム名: ユーザーID 整数値, x 整数値, y 整数値, layer 階層
            await cur.execute("CREATE TABLE IF NOT EXISTS position(user_id BIGINT(20), x INT, y INT, layer INT)")
            await conn.commit()

            # テーブル名:『item』 カラム内容： ユーザーID 整数型, アイテムID　整数値, 個数 整数値
            await cur.execute("CREATE TABLE IF NOT EXISTS item(user_id BIGINT(20), item_id INT, count INT)")
            await conn.commit()

            # テーブル名:『ban_user』 カラム内容： ユーザーID 整数型
            await cur.execute("CREATE TABLE IF NOT EXISTS ban_user(user_id BIGINT(20))")
            await conn.commit()

            # テーブル名:『mine』カラム内容: ユーザーID 整数値, x 整数値, y 整数値, layer 階層
            await cur.execute("CREATE TABLE IF NOT EXISTS mine(user_id BIGINT(20), x INT, y INT, layer INT)")
            await conn.commit()

            # テーブル名:『treasure』カラム内容: ユーザーID 整数値, x 整数値, y 整数値, layer 階層
            await cur.execute("CREATE TABLE IF NOT EXISTS treasure(user_id BIGINT(20), x INT, y INT, layer INT)")
            await conn.commit()
            
            # テーブル名:『monster』カラム内容: ユーザーID 整数値, x 整数値, y 整数値, layer 階層
            await cur.execute("CREATE TABLE IF NOT EXISTS monster(user_id BIGINT(20), x INT, y INT, layer INT)")
            await conn.commit()
            
            # テーブル名:『warp_point』カラム内容: ユーザーID 整数値, x 整数値, y 整数値, layer 階層
            await cur.execute("CREATE TABLE IF NOT EXISTS warp_point(user_id BIGINT(20), x INT, y INT, layer INT)")
            await conn.commit()

            # テーブル名:『shop』カラム内容: ユーザーID 整数値, x 整数値, y 整数値, layer 階層
            await cur.execute("CREATE TABLE IF NOT EXISTS shop(user_id BIGINT(20), x INT, y INT, layer INT)")
            await conn.commit()
asyncio.run(create_database())
