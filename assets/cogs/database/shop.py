import random
import asyncio
from aiosqlite import connect
import discord


class Shop:
    def __init__(self, ctx=None, interaction=None, config=None):
        self.ctx = ctx
        self.interaction = interaction
        self.ctxInt = ctx if ctx else interaction
        self.user = self.ctx.author if self.ctx else self.interaction.user
        self.user_id = self.user.id
        self.config = config

    async def shop(self):
        embed = discord.Embed(description="いらっしゃーい")
        msg = await self.ctxInt.send(embed=embed)
        try:
            msg_react = await self.bot.wait_for(
                "message", check=lambda m: m.author == self.ctxInt.author, timeout=30
            )
            if msg_react.content == "y":
                embed = discord.Embed(description="どれかう")
                await msg.edit(embed=embed)
                return

            elif msg_react.content == "n":
                embed = discord.Embed(description="ばいばい")
                await msg.edit(embed=embed)
                return

        except asyncio.TimeoutError:
            return await msg.edit(content="timeout")

    async def buy(self):
        pass

    async def sell(self):
        pass

    async def talk(self):
        pass

    async def get_shop_point(self, layer):
        db_path = self.bot.config.get_db()
        async with connect(db_path) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT x, y FROM shop WHERE user_id=? AND layer=?",
                    (self.user_id, layer),
                )
                shop_pos = await cur.fetchall()
                if not shop_pos:
                    for i in self.generate_shop_point():
                        await cur.execute(
                            "INSERT INTO shop values(?,?,?,?)",
                            (self.user_id, i[0], i[1], layer),
                        )
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
