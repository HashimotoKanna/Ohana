from PIL import Image

step_list = [1, 2, 3, 2]
background_img = Image.open('img/background.png')


def add_image_to_list(step_list, direction):
    new_img_list = []
    for i in step_list:
        pic_name = f'img/player0_{direction}{i}.png'
        img = Image.open(pic_name)
        img = img.resize(((img.width - 8), (img.height - 8)))
        background_img.paste(img, (220, 200))
        new_img_list.append(background_img.copy())
    return new_img_list


def create_animation(step_list, direction):
    images = add_image_to_list(step_list, direction)
    images[0].save(f'img/playing_{direction}.gif', save_all=True, optimize=False, append_images=images[1:], duration=500,
                   loop=0, quality=95)


create_animation(step_list, 'front')
create_animation(step_list, 'left')
create_animation(step_list, 'right')
create_animation(step_list, 'back')
