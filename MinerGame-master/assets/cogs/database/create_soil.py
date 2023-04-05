from PIL import Image, ImageDraw
import random

soil_color = (169, 110, 45)
add_colors = (
    (181, 115, 67),
    (181, 116, 67),
    (181, 102, 45),
    (209, 132, 77),
    (181, 135, 67)

)
underground_color_line = (129, 70, 5)


soil_size = (48,48)
img = Image.new("RGB", soil_size, soil_color)
draw = ImageDraw.Draw(img)
for i in range(48 * 48):
    x = random.randint(0, 48)
    y = random.randint(0, 48)
    draw.point((x, y), fill=random.choice(add_colors))

img.save('img/soil.png')