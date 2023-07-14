import random
from aiosqlite import connect


class Monster:
    def __init__(self, ctx=None, interaction=None, config=None):
        self.ctx = ctx
        self.interaction = interaction
        self.user = self.ctx.author if self.ctx else self.interaction.user
        self.user_id = self.user.id
        self.config = config

    async def get_monster_point(self, layer):
        db_path = self.config.get_db()
        async with connect(db_path) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT x, y FROM monster WHERE user_id=? AND layer=?",
                    (self.user_id, layer),
                )
                monster_points = await cur.fetchall()
                if not monster_points:
                    for i in self.generate_monster_points():
                        await cur.execute(
                            "INSERT INTO monster values(?,?,?,?)",
                            (self.user_id, i[0], i[1], layer),
                        )
                        await conn.commit()
                        monster_points.append((i[0], i[1]))
                return monster_points

    def generate_monster_points(self) -> list:
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
