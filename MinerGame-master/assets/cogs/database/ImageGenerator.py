from PIL import Image
import io
import requests
from .treasure import Treasure

IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_0_PATH = f'{IMG_PATH}/background_0.png'
BG_1_PATH = f'{IMG_PATH}/background_1.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'
TREASUREBOX_PATH = f'{IMG_PATH}/treasure_box.png'


class ImageGenerator:
    def __init__(self, ctx=None, interaction=None):
        self.ctx = ctx
        self.interaction = interaction
        self.user = self.ctx.author if self.ctx else self.interaction.user
        self.user_id = self.user.id
        self.none_img = Image.open(NONE_PATH)
        self.treasure_box_img = Image.open(TREASUREBOX_PATH)

    async def make_terrain(self, pos, mines, layer):

        none_img = Image.open(NONE_PATH)
        img = Image.open(io.BytesIO(requests.get(self.user.display_avatar).content))
        img = img.resize((34, 34))
        t_img = Image.open(TREASUREBOX_PATH)
        t_img = t_img.resize((40, 40))
        background_img = change_background(layer)
        mine_pos = []
        for m_x, m_y in mines:
            mine_pos.append((m_x, m_y))
        if mine_pos:
            for x, y in mine_pos:
                x_pos = 480 + x * 40
                y_pos = y * 40
                background_img.paste(none_img, (x_pos, y_pos))

        treasure = Treasure(ctx=self.ctx, interaction=self.interaction)
        treasure_pos = await treasure.get_treasure_point(layer)
        for t_pos in treasure_pos:
            x = int(t_pos[0] * 40)
            y = int(t_pos[1] * 40)
            background_img.paste(t_img, (x, y))

        x = pos[0] * 40 + 480 + 3
        y = pos[1] * 40 + 3
        #   self.create_animation("front", x, y)
        background_img.paste(img, (x, y))
        background_img.save(f'{IMG_PATH}' + f'/playing_{self.user_id}.png', quality=95)

    def generate_mine_pos(self, mines):
        mine_pos = []
        for m_x, m_y in mines:
            mine_pos.append((m_x, m_y))
        if mine_pos:
            for x, y in mine_pos:
                x_pos = 480 + x * 40
                y_pos = y * 40
        for i in mines:
            mine_pos.append()



def change_background(layer):
    if layer == 1:
        return Image.open(BG_0_PATH)
    else:
        background_img = Image.open(BG_1_PATH)
    return background_img
