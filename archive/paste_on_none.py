from PIL import Image
import traceback

DB_PATH = 'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/db/mine.db'
BG_PATH = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img/background.png'
NONE_PATH = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img/none.png'
BG_TEMP_PATH = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img/background_temp.png'

def add_image_to_list(direction, x, y):
    step_list = [1, 2, 3, 2]
    background_img = Image.open(BG_PATH)
    new_img_list = []
    for i in step_list:
        pic_name = f'img/player0_{direction}{i}.png'
        img = Image.open(pic_name)
        img = img.resize(((img.width - 8), (img.height - 8)))
        background_img.paste(img, (x, y))
        new_img_list.append(background_img.copy())
    return new_img_list


def create_animation(direction, x, y):
    images = add_image_to_list(direction, x, y)
    images[0].save(f'img/playing_{direction}.gif', save_all=True, optimize=False, append_images=images[1:],
                   duration=500,
                   loop=0, quality=95)


def paste_on_none():
    try:
        player = 10
        x = 220
        y = 200
        img = Image.open(NONE_PATH)
        background_img = Image.open(BG_PATH)
        i_x = img.width - 8
        i_y = img.height - 8
        for _ in range(player - 1):
            img = img.resize((i_x, i_y))
            background_img.paste(img, (x, y))
            y += 40
        background_img.save(BG_TEMP_PATH, quality=95)

      #  create_animation("front", x, y)

    except:
        print("エラー情報\n" + traceback.format_exc())


paste_on_none()
