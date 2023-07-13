import random
from aiosqlite import connect


class Treasure:
    def __init__(self, ctx=None, interaction=None, config=None):
        self.ctx = ctx
        self.interaction = interaction
        self.user = self.ctx.author if self.ctx else self.interaction.user
        self.user_id = self.user.id
        self.config = config

    async def get_treasure_point(self, layer):
        db_path = self.bot.config.get_db()
        async with connect(db_path) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT x, y FROM treasure WHERE user_id=? AND layer=?",
                    (self.user_id, layer),
                )
                treasure_points = await cur.fetchall()
                if not treasure_points:
                    for i in self.generate_treasure_points():
                        await cur.execute(
                            "INSERT INTO treasure values(?,?,?,?)",
                            (self.user_id, i[0], i[1], layer),
                        )
                        await conn.commit()
                        treasure_points.append((i[0], i[1]))
                return treasure_points

    def generate_treasure_points(self) -> list:
        x = 25
        y = 20
        pos_list = []
        tmp = []
        for i in range(x):
            for j in range(y):
                tmp.append([i, j])
        for _ in range(8):
            pos_list.append(random.choice(tmp))
        return pos_list
