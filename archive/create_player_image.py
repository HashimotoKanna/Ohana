from PIL import Image, ImageDraw
import time
underground_color = (169, 110, 45)
underground_color_line = (129, 70, 5)
ground_color = (0, 170, 0)
ground_color_line = (0, 140, 0)

step = 48
x0 = 0
x1 = 0
y0 = 0
y1 = 0
counter = 0
p_n = 0

y0 = step + step + step
y1 = step + step + step + step


for j in range(12):

    if counter > 2:
        counter = 0
        p_n += 1
    counter += 1
    direct = [f'_front{counter}.png', f'_left{counter}.png', f'_right{counter}.png', f'_back{counter}.png']
    x1 += step
    img = Image.open('img/players.png')
    img = img.crop((x0, y0, x1, y1))
    x0 += step
    img.save(f'img/player{p_n}' + direct[3], quality=95)
counter = 0
p_n = 0
x0 = 0
x1 = 0

img.show()
