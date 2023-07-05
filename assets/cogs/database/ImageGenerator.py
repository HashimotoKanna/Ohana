from PIL import Image
import io
import requests
from .treasure import Treasure
from .shop import Shop
from .player import Player
from .monster import Monster
from typing import List, Tuple
import traceback
import json
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
BG_0_PATH = paths_list["IMG_PATH"] + paths_list["BG_0_PATH"]
BG_1_PATH = paths_list["IMG_PATH"] + paths_list["BG_1_PATH"]
NONE_PATH = paths_list["IMG_PATH"] + paths_list["NONE_PATH"]
BG_TMP_PATH = paths_list["IMG_PATH"] + paths_list["BG_TMP_PATH"]
TREASURE_BOX_PATH = paths_list["IMG_PATH"] + paths_list["TREASURE_BOX_PATH"]
SHOP_PATH = paths_list["IMG_PATH"] + paths_list["SHOP_PATH"]
AKUMA_PATH = paths_list["IMG_PATH"] + paths_list["AKUMA_PATH"]

class ImageGenerator(Player):
    def __init__(self, ctx=None, interaction=None):
        super().__init__(ctx, interaction)
        self.none_img = Image.open(NONE_PATH)
        self.treasure_box_img = Image.open(TREASURE_BOX_PATH)

    async def make_terrain(self, player_pos: Tuple, mines_pos: List[Tuple[int, int]], layer: int) -> None:
        try:

            none_img = Image.open(NONE_PATH)
            shop_img = Image.open(SHOP_PATH).resize((40, 40))
            player_img = Image.open(io.BytesIO(requests.get(self.user.display_avatar).content)).resize((34, 34))
            treasure_img = Image.open(TREASURE_BOX_PATH).resize((40, 40))
            background_img = change_background(layer)
            monster_img = Image.open(AKUMA_PATH).resize((40, 40))

            treasure = Treasure(ctx=self.ctx, interaction=self.interaction)
            shop = Shop(ctx=self.ctx, interaction=self.interaction)
            monster = Monster(ctx=self.ctx, interaction=self.interaction)

            background_img = self.conversion_pos(background_img, none_img, mines_pos, center=True) #掘ったところの画像をはる
            background_img = self.conversion_pos(background_img, treasure_img, await treasure.get_treasure_point(layer), center=False) #宝のある場所に画像をはる
            background_img = self.conversion_pos(background_img, shop_img, await shop.get_shop_point(layer), center=False) #店のある場所に画像をはる
            background_img = self.conversion_pos(background_img, player_img, [player_pos], center=True)#プレイヤーの画像をはる
            background_img = self.conversion_pos(background_img, monster_img, await monster.get_monster_point(layer), center=False)#monsterの画像をはる
            
            background_img.save(f'{IMG_PATH}' + f'/playing_{self.user_id}.png', quality=95)
        except:
            print("エラー情報\n" + traceback.format_exc())

    def conversion_pos(self, background_img, img, old_pos, center=False):
        if old_pos:
            for x, y in old_pos:
                background_img.paste(img, ((480 if center else 0) + x * 40, y * 40))
        return background_img


def change_background(layer):
    if layer == 1:
        return Image.open(BG_0_PATH)
    else:
        background_img = Image.open(BG_1_PATH)
    return background_img
