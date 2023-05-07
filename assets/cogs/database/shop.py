import random
import asyncio
from aiosqlite import connect

DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"


class Shop:
    def __init__(self, ctx=None, interaction=None):
        self.ctx = ctx
        self.interaction = interaction
        self.user = self.ctx.author if self.ctx else self.interaction.user
        self.user_id = self.user.id

    async def buy(self):
        pass

    async def sell(self):
        pass

    async def talk(self):
        pass

    async def get_shop_point(self, layer):
        async with connect(DB_PATH) as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT x, y FROM shop WHERE user_id=? AND layer=?", (self.user_id, layer))
                shop_pos = await cur.fetchall()
                if not shop_pos:
                    for i in self.generate_shop_point():
                        await cur.execute("INSERT INTO shop values(?,?,?,?)", (self.user_id, i[0], i[1], layer))
                        await conn.commit()
                        shop_pos.append((i[0], i[1]))
                return shop_pos

    def generate_shop_point(self) -> list:
        x = 25
        y = 20
        pos_list = []
        tmp = []
        for i in range(x):
            for j in range(y):
                tmp.append([i, j])
        pos_list.append(random.choice(tmp))
        return pos_list
