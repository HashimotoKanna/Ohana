from PIL import Image
import io
import requests
import random
from .player import Player

IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_0_PATH = f'{IMG_PATH}/background_0.png'
BG_1_PATH = f'{IMG_PATH}/background_1.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'
TREASUREBOX_PATH = f'{IMG_PATH}/treasure_box.png'


class Mine(Player):
    def __init__(self, ctx=None, interaction=None):
        super().__init__(ctx, interaction)
        self.none_img = Image.open(NONE_PATH)
        self.treasure_box_img = Image.open(TREASUREBOX_PATH)

    async def player_mine(self, m_x: int, m_y: int, conn, cur):
        x, y, layer = await self.get_player_position(conn, cur)

        if m_x + x >= 20:
            return (x, y), "横にはこれ以上掘れないよ！", layer
        x += m_x

        y, layer = is_change_layer(y, m_y, layer)

        mines = await self.get_player_mine(cur, layer)
        await self.make_terrain((x, y), mines, layer)

        is_mine = f"{abs(m_y if m_y != 0 else m_x)}つ" + await self.move(x, y, layer, cur, conn, mines)  # 斜め移動をする場合ここ絶対エラー出る
        return (x, y), is_mine, layer

    def paste_icon(self, x, y):
        background_img = Image.open(BG_TMP_PATH)
        img = Image.open(io.BytesIO(requests.get(self.user.display_avatar).content))
        img = img.resize((40, 40))
        background_img.paste(img, (x, y))
        background_img.save(f'{IMG_PATH}' + f'/playing_{self.user_id}.png', quality=95)

    async def make_terrain(self, pos, mines, layer):
        mine_pos = []
        for m_x, m_y in mines:
            mine_pos.append((m_x, m_y))
        none_img = Image.open(NONE_PATH)
        img = Image.open(io.BytesIO(requests.get(self.user.display_avatar).content))
        img = img.resize((34, 34))
        t_img = Image.open(TREASUREBOX_PATH)
        t_img = t_img.resize((40, 40))
        background_img = change_background(layer)

        if mine_pos:
            for x, y in mine_pos:
                x_pos = 480 + x * 40
                y_pos = y * 40
                background_img.paste(none_img, (x_pos, y_pos))

        treasure_pos = generate_treasure_point()
        for t_pos in treasure_pos:
            x = int(t_pos[0] * 40)
            y = int(t_pos[1] * 40)
            background_img.paste(t_img, (x, y))

        x = pos[0] * 40 + 480 + 3
        y = pos[1] * 40 + 3
        #   self.create_animation("front", x, y)
        background_img.paste(img, (x, y))
        background_img.save(f'{IMG_PATH}' + f'/playing_{self.user_id}.png', quality=95)


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


def change_background(layer):
    if layer == 1:
        background_img = Image.open(BG_0_PATH)
    else:
        background_img = Image.open(BG_1_PATH)
    return background_img


def generate_treasure_point():
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
