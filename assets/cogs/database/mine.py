from PIL import Image
import io
import json
import requests
import random
from .player import Player
from .treasure import Treasure
from .shop import Shop
from .ImageGenerator import ImageGenerator


def get_path():
    with open('assets/config/paths.json', encoding='utf-8') as fh:
        json_txt = fh.read()
        json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
        paths_list = json.loads(json_txt)
        return paths_list


paths_list = get_path()

IMG_PATH = paths_list["ABS_PATH"] + paths_list["IMG_PATH"]
DB_PATH = paths_list["ABS_PATH"] + paths_list["DB_PATH"]
BG_PATH = paths_list["IMG_PATH"] + paths_list["BG_PATH"]
NONE_PATH = paths_list["IMG_PATH"] + paths_list["NONE_PATH"]
BG_TMP_PATH = paths_list["IMG_PATH"] + paths_list["BG_TMP_PATH"]
TREASURE_BOX_PATH = paths_list["IMG_PATH"] + "treasure_box.png"

class Mine(Player):
    def __init__(self, ctx=None, interaction=None):
        super().__init__(ctx, interaction)
        self.none_img = Image.open(NONE_PATH)
        self.treasure_box_img = Image.open(TREASURE_BOX_PATH)

    async def player_mine(self, m_x: int, m_y: int, conn, cur):
        treasure = Treasure(ctx=self.ctx, interaction=self.interaction)
        shop = Shop(ctx=self.ctx, interaction=self.interaction)

        x, y, layer = await self.get_player_position(conn, cur)
        treasure_pos = await treasure.get_treasure_point(layer)
        shop_pos = await shop.get_shop_point(layer)
        terrain = ImageGenerator(ctx=self.ctx, interaction=self.interaction)
        if m_x + x >= 20:
            return (x, y), "横にはこれ以上掘れないよ！", layer
        x += m_x

        y, layer = is_change_layer(y, m_y, layer)

        mines = await self.get_player_mine(cur, layer)
        await terrain.make_terrain((x, y), mines, layer)

        is_mine = f"{abs(m_y if m_y != 0 else m_x)}つ" + await self.move(x, y, layer, cur, conn,
                                                                        mines)  # 斜め移動をする場合ここ絶対エラー出る
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
