from PIL import Image, ImageDraw

underground_color = (169, 110, 45)
underground_color_line = (129, 70, 5)
ground_color = (0, 170, 0)
ground_color_line = (0, 140, 0)

IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_PATH = f'{IMG_PATH}/background.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'

soil_path=IMG_PATH+"/soil.png"
grass_path=IMG_PATH+"/grass.png"
background_size = (1000, 800)
img = Image.new("RGB", background_size, (0,0,0))
draw = ImageDraw.Draw(img)
soil_img = Image.open(soil_path)
soil_img = soil_img.resize(((soil_img.width - 8), (soil_img.height - 8)))

grass_img = Image.open(grass_path)
grass_img = grass_img.resize((40, 40))

none_img = Image.open(NONE_PATH)
none_img = none_img.resize((40, 40))
i_s = 0
j_s = 0
for i in range(background_size[0] // 40):
    for j in range(background_size[1] // 40):
        img.paste(soil_img, (i_s, j_s))
        j_s += 40
    i_s += 40
    j_s = 0
i_s = 0
j_s = 40
for _ in range(background_size[0] // 40):
    img.paste(grass_img, (i_s, j_s))
    i_s += 40

i_s = 0
j_s = 0
for _ in range(background_size[0] // 40):
    img.paste(none_img, (i_s, j_s))
    i_s += 40

img.save(IMG_PATH+'/background_0.png', quality=95)