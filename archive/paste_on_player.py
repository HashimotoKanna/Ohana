from PIL import Image
IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_PATH = f'{IMG_PATH}/background.jpg'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.jpg'
step_list = [1, 2, 3, 2]
background_img = Image.open(f'{IMG_PATH}/background.jpg')


def add_image_to_list(step_list, direction):
    new_img_list = []
    for i in step_list:
        background_img = Image.open(f'{IMG_PATH}/background.jpg')
        try:
            pic_name = f'{IMG_PATH}/player_0_{direction}{i}b.png'
            img = Image.open(pic_name)
        except:
            pic_name = f'{IMG_PATH}/player_0_{direction}{i}b.png'
            img = Image.open(pic_name)
        img = img.resize(((img.width - 8), (img.height - 8)))
        background_img.paste(img, (0, 0))
        if background_img.mode != "RGB":
            background_img = background_img.convert("RGB")
        background_img.save(r"C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img/"+f"{i}b.png")

        new_img_list.append(background_img.copy())
    return new_img_list


def create_animation(step_list, direction):
    images = add_image_to_list(step_list, direction)
    images[0].save(f'{IMG_PATH}/playing_{direction}.gif', save_all=True, optimize=False, append_images=images[1:], duration=500,
                   loop=0, quality=95)


create_animation(step_list, 'front')
create_animation(step_list, 'left')
create_animation(step_list, 'right')
create_animation(step_list, 'back')
