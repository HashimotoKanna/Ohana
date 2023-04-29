import traceback
from PIL import Image
import io
import requests
import random

IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_0_PATH = f'{IMG_PATH}/background_0.png'
BG_1_PATH = f'{IMG_PATH}/background_1.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'
TREASUREBOX_PATH = f'{IMG_PATH}/treasure_box.png'


class Mine:
    def __init__(self, ctx=None, interaction=None):
        self.ctx = ctx
        self.interaction = interaction
        self.user_id = self.ctx.author.id if self.ctx else self.interaction.user.id if self.interaction else None
        self.user = self.ctx.author if self.ctx else self.interaction.user if self.interaction else None

    async def player_mine(self, user_id: int, m_x: int, m_y: int, conn, cur):
        try:
            is_mine = "一マス移動しました！"
            x, y, layer = await self.get_player_position(user_id, conn, cur)

            if m_x + x >= 20:
                return (x, y), "横にはこれ以上掘れないよ！", layer
            x += m_x

            y, layer = is_change_layer(y, m_y, layer)

            mines = await self.get_player_mine(user_id, layer, cur)
            await self.make_terrain((x, y), mines, layer)

            if not (x, y) in mines:
                await cur.execute("INSERT INTO mine values(?,?,?,?)", (user_id, x, y, layer))
                await conn.commit()
                is_mine = "一マス掘りました！"

            await cur.execute("UPDATE position SET x=?, y=?, layer=? WHERE user_id=?", (x, y, layer, user_id))
            await conn.commit()
            return (x, y), is_mine, layer
        except:
            print("エラー情報\n" + traceback.format_exc())

    def paste_icon(self, x, y):
        background_img = Image.open(BG_TMP_PATH)
        img = Image.open(io.BytesIO(requests.get(self.user.display_avatar).content))
        img = img.resize((40, 40))
        background_img.paste(img, (x, y))
        background_img.save(f'{IMG_PATH}' + f'/playing_{self.user_id}.png', quality=95)

    async def make_terrain(self, pos, mines, layer):
        try:
            mine_pos = []
            for m_x, m_y in mines:
                mine_pos.append((m_x, m_y))
            none_img = Image.open(NONE_PATH)
            t_img = Image.open(TREASUREBOX_PATH)
            t_img = t_img.resize((40, 40))
            background_img = change_background(layer)

            i_x = none_img.width - 8
            i_y = none_img.height - 8
            none_img = none_img.resize((i_x, i_y))
            if mine_pos:
                for x, y in mine_pos:
                    x_pos = 500 + x * 40  # 真ん中なので1000の2割った500からスタート
                    y_pos = y * 40
                    background_img.paste(none_img, (x_pos, y_pos))

            treasure_pos = generate_treasure_point()
            for t_pos in treasure_pos:
                t_pos[0] *= 40
                t_pos[1] *= 40
                background_img.paste(t_img, t_pos)

            x = pos[0] * 40 + 500
            y = pos[1] * 40
            self.create_animation(x, y)

        except:
            print("エラー情報\n" + traceback.format_exc())

    async def get_player_position(self, user_id, conn, cur):
        try:
            await cur.execute("SELECT x, y, layer FROM position WHERE user_id=?", (user_id,))
            player = await cur.fetchone()
            if not player:
                await cur.execute("INSERT INTO position values(?,?,?,?)", (user_id, 0, 0, 1))
                await conn.commit()
                await cur.execute("INSERT INTO mine values(?,?,?,?)", (user_id, 0, 0, 1))
                await conn.commit()
                return 0, 0, 1
            return player
        except:
            print("エラー情報\n" + traceback.format_exc())

    async def get_player_mine(self, user_id, layer, cur):
        try:
            await cur.execute("SELECT x, y FROM mine WHERE user_id=? AND layer=?", (user_id, layer))
            player = await cur.fetchall()
            return player
        except:
            print("エラー情報\n" + traceback.format_exc())


def is_change_layer(y, m_y, layer):
    judge = y + m_y > 19 if layer == 1 else y + m_y > 20
    if judge:
        layer += 1
        y %= 19
    elif y + m_y < 0:
        y = 20
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
