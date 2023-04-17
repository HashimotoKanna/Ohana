from PIL import Image, ImageDraw
import random
IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
soil_color = (131, 255, 54)
add_colors = (
    (116 ,227 ,48),
    (120, 235, 49),
    (118, 255, 84),
    (148, 255, 82),
    (140, 255, 69)
)



soil_size = (40,40)
img = Image.new("RGB", soil_size, soil_color)
draw = ImageDraw.Draw(img)
for i in range(48 * 48):
    x = random.randint(0, 48)
    y = random.randint(0, 48)
    draw.point((x, y), fill=random.choice(add_colors))

img.save(IMG_PATH + '/grass.png')