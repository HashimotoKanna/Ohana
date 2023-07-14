from PIL import Image
import io
import requests
from .treasure import Treasure
from .shop import Shop
from .player import Player
from .monster import Monster
from typing import List, Tuple
import traceback


class ImageGenerator(Player):
    def __init__(self, ctx=None, interaction=None, config=None):
        super().__init__(ctx, interaction)
        self.config = config

    async def make_terrain(
        self, player_pos: Tuple, mines_pos: List[Tuple[int, int]], layer: int
    ) -> None:
        try:
            none_path = self.config.get_none()
            shop_path = self.config.get_shop()
            treasure_box_path = self.config.get_treasure_box()
            akuma_path = self.config.get_akuma()
            playing_path = self.config.get_playing(self.user_id)

            none_img = Image.open(none_path)
            shop_img = Image.open(shop_path).resize((40, 40))
            player_img = Image.open(
                io.BytesIO(requests.get(self.user.display_avatar).content)
            ).resize((34, 34))
            treasure_img = Image.open(treasure_box_path).resize((40, 40))
            background_img = self.change_background(layer)
            monster_img = Image.open(akuma_path).resize((40, 40))

            treasure = Treasure(
                ctx=self.ctx, interaction=self.interaction, config=self.config
            )
            shop = Shop(ctx=self.ctx, interaction=self.interaction, config=self.config)
            monster = Monster(
                ctx=self.ctx, interaction=self.interaction, config=self.config
            )

            background_img = self.conversion_pos(
                background_img, none_img, mines_pos, center=True
            )  # 掘ったところの画像をはる
            background_img = self.conversion_pos(
                background_img,
                treasure_img,
                await treasure.get_treasure_point(layer),
                center=False,
            )  # 宝のある場所に画像をはる
            background_img = self.conversion_pos(
                background_img, shop_img, await shop.get_shop_point(layer), center=False
            )  # 店のある場所に画像をはる
            background_img = self.conversion_pos(
                background_img, player_img, [player_pos], center=True
            )  # プレイヤーの画像をはる
            background_img = self.conversion_pos(
                background_img,
                monster_img,
                await monster.get_monster_point(layer),
                center=False,
            )  # monsterの画像をはる

            background_img.save(playing_path, quality=95)
        except:
            print("エラー情報\n" + traceback.format_exc())

    def conversion_pos(self, background_img, img, old_pos, center=False):
        if old_pos:
            for x, y in old_pos:
                background_img.paste(img, ((480 if center else 0) + x * 40, y * 40))
        return background_img

    def change_background(self, layer):
        bg0_path = self.config.get_bg(0)
        bg1_path = self.config.get_bg(1)
        if layer == 1:
            return Image.open(bg0_path)
        else:
            background_img = Image.open(bg1_path)
        return background_img
