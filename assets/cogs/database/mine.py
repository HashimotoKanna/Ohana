from .monster import Monster
from .player import Player
from .treasure import Treasure
from .shop import Shop
from .ImageGenerator import ImageGenerator


class Mine(Player):
    def __init__(self, ctx=None, interaction=None, config=None):
        super().__init__(ctx, interaction)
        self.config = config

    async def player_mine(self, m_x: int, m_y: int, conn, cur):
        x, y, layer = await self.get_player_position(conn, cur)
        terrain = ImageGenerator(ctx=self.ctx, interaction=self.interaction)
        if m_x + x >= 20:
            return (x, y), "横にはこれ以上掘れないよ！", layer
        x += m_x

        y, layer = is_change_layer(y, m_y, layer)

        mines = await self.get_player_mine(cur, layer)
        await terrain.make_terrain((x, y), mines, layer)

        is_mine = f"{abs(m_y if m_y != 0 else m_x)}つ" + await self.move(
            x, y, layer, cur, conn, mines
        )
        return (x, y), is_mine, layer


def is_change_layer(y, m_y, layer):
    if y + m_y > 19:  # 20を突破するなら
        layer += 1
        y = 0
    elif y + m_y < 0:
        y = 19
        layer -= 1
    else:
        y += m_y
    return y, layer
