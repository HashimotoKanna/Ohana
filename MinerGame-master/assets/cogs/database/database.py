import traceback
from PIL import Image

IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_PATH = f'{IMG_PATH}/background.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'


def add_image_to_list(direction, x, y):
    step_list = [1, 2, 3, 2]
    background_img = Image.open(BG_TMP_PATH)
    new_img_list = []
    for i in step_list:
        pic_name = f'{IMG_PATH}' + f'/player0_{direction}{i}.png'
        img = Image.open(pic_name)
        img = img.resize(((img.width - 8), (img.height - 8)))
        background_img.paste(img, (x, y))
        new_img_list.append(background_img.copy())
    return new_img_list


def create_animation(direction, x, y):
    images = add_image_to_list(direction, x, y)
    images[0].save(f'{IMG_PATH}' + f'/playing_{direction}.gif', save_all=True, optimize=False, append_images=images[1:],
                   duration=500,
                   loop=0, quality=95)


async def player_mine(user_id, m_x, m_y, conn, cur):
    try:
        x, y = await get_player_position(user_id, conn, cur)
        x += m_x
        y += m_y
        mines = await get_player_mine(user_id, conn, cur)
        await make_terrain((x, y), mines)
        await cur.execute("UPDATE mine SET x=?, y=? WHERE user_id=?", (x, y, user_id))
        await conn.commit()
        return x, y
    except:
        print("エラー情報\n" + traceback.format_exc())


async def make_terrain(pos, mines):
    try:
        player_x = pos[0] if pos[0] < 25 else pos[0] % 25
        player_y = pos[1] if pos[1] < 25 else pos[1] % 25
        mine_pos = []
        for m_x, m_y in mines:
            if m_x-25 < pos[0] < m_x+25 and m_y-20 < pos[1] < m_y+20:
                mine_pos.append((m_x, m_y))
        none_img = Image.open(NONE_PATH)
        background_img = Image.open(BG_PATH)
        i_x = none_img.width - 8
        i_y = none_img.height - 8
        none_img = none_img.resize((i_x, i_y))
        for x, y in mine_pos:
            x_pos = x * 40
            y_pos = y * 40
            background_img.paste(none_img, (x_pos, y_pos))
        background_img.save(BG_TMP_PATH, quality=95)

        create_animation("front", player_x, player_y)

    except:
        print("エラー情報\n" + traceback.format_exc())


async def get_player_position(user_id, conn, cur):
    try:
        await cur.execute("SELECT x, y FROM position WHERE user_id=?", (user_id,))
        player = await cur.fetchone()
        if not player:
            await cur.execute("INSERT INTO position values(?,?,?,?)", (user_id, 0, 1, 1))
            await conn.commit()
            await cur.execute("INSERT INTO mine values(?,?,?,?)", (user_id, 0, 1, 1))
            await conn.commit()
            return 0, 1
        return player
    except:
        print("エラー情報\n" + traceback.format_exc())


async def get_player_mine(user_id, conn, cur):
    try:
        await cur.execute("SELECT x, y FROM mine WHERE user_id=?", (user_id,))
        player = await cur.fetchall()
        if not player:
            await cur.execute("INSERT INTO position values(?,?,?,?)", (user_id, 0, 1, 1))
            await conn.commit()
            await cur.execute("INSERT INTO mine values(?,?,?,?)", (user_id, 0, 1, 1))
            await conn.commit()
            return 0, 1
        return player
    except:
        print("エラー情報\n" + traceback.format_exc())
