from PIL import Image
import io
import requests
from .treasure import Treasure
from .shop import Shop
from .player import Player
from typing import List, Tuple
import traceback

IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_0_PATH = f'{IMG_PATH}/background_0.png'
BG_1_PATH = f'{IMG_PATH}/background_1.png'
NONE_PATH = f'{IMG_PATH}/none.png'
SHOP_PATH = f'{IMG_PATH}/shop.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'
TREASUREBOX_PATH = f'{IMG_PATH}/treasure_box.png'


class ImageGenerator(Player):
    def __init__(self, ctx=None, interaction=None):
        super().__init__(ctx, interaction)
        self.none_img = Image.open(NONE_PATH)
        self.treasure_box_img = Image.open(TREASUREBOX_PATH)

    async def make_terrain(self, player_pos: Tuple, mines_pos: List[Tuple[int, int]], layer: int) -> None:
        try:

            none_img = Image.open(NONE_PATH)
            shop_img = Image.open(SHOP_PATH).resize((40, 40))
            player_img = Image.open(io.BytesIO(requests.get(self.user.display_avatar).content)).resize((34, 34))
            treasure_img = Image.open(TREASUREBOX_PATH).resize((40, 40))
            background_img = change_background(layer)

            treasure = Treasure(ctx=self.ctx, interaction=self.interaction)
            shop = Shop(ctx=self.ctx, interaction=self.interaction)

            background_img = self.conversion_pos(background_img, none_img, mines_pos, center=True)
            background_img = self.conversion_pos(background_img, treasure_img, await treasure.get_treasure_point(layer), center=False)
            background_img = self.conversion_pos(background_img, shop_img, await shop.get_shop_point(layer), center=False)
            background_img = self.conversion_pos(background_img, player_img, [player_pos], center=True)

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
