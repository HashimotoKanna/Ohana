async def get_player_items(self, user_id, conn, cur):
    await cur.execute("SELECT item_id, count FROM item WHERE user_id=?", (user_id,))
    i_list = ''.join(f'{self.bot.item_lists[i[0]]} : {i[1]}個\n' for i in await cur.fetchall())