class Player:
    def __init__(self, ctx=None, interaction=None):
        self.ctx = ctx
        self.interaction = interaction
        self.user_id = self.ctx.author.id if self.ctx else self.interaction.user.id if self.interaction else None
        self.user = self.ctx.author if self.ctx else self.interaction.user if self.interaction else None

    async def move(self, x, y, layer, cur, conn, mines=None):
        is_mine = "移動しました！"
        if mines and not (x, y) in mines:
            await cur.execute("INSERT INTO mine values(?,?,?,?)", (self.user_id, x, y, layer))
            await conn.commit()
            is_mine = "掘りました！"

        await cur.execute("UPDATE position SET x=?, y=?, layer=? WHERE user_id=?", (x, y, layer, self.user_id))
        await conn.commit()
        return is_mine

    async def get_player_position(self, conn, cur):
        await cur.execute("SELECT x, y, layer FROM position WHERE user_id=?", (self.user_id,))
        player = await cur.fetchone()
        if not player:
            await cur.execute("INSERT INTO position values(?,?,?,?)", (self.user_id, 0, 0, 1))
            await conn.commit()
            await cur.execute("INSERT INTO mine values(?,?,?,?)", (self.user_id, 0, 0, 1))
            await conn.commit()
            return 0, 0, 1
        return player

    async def get_player_mine(self, cur, layer=None):
        if layer:
            await cur.execute("SELECT x, y FROM mine WHERE user_id=? AND layer=?", (self.user_id, layer))
            player = await cur.fetchall()
            return player

        else:
            await cur.execute("SELECT x, y, layer FROM mine WHERE user_id=?", (self.user_id,))
            player = await cur.fetchall()
            return player

    async def get_player_warp_point(self, cur):
        await cur.execute("SELECT x, y, layer FROM mine WHERE user_id=?", (self.user_id,))
        player = await cur.fetchall()
        return player

