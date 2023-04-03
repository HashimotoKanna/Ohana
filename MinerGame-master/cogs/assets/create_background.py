from PIL import Image, ImageDraw

underground_color = (169, 110, 45)
underground_color_line = (129, 70, 5)
ground_color = (0, 170, 0)
ground_color_line = (0, 140, 0)
background_size = (1000, 800)
img = Image.new("RGB", background_size, (0, 0, 0))
draw = ImageDraw.Draw(img)
for i in range(background_size[0] // 10):
    s = i * 10
    for j in range(background_size[1] // 10):
        d = j * 10
        draw.rectangle((0 + s, 220 + d, 20 + s, 200 + d), fill=underground_color, outline=underground_color_line)
for i in range(background_size[0] // 10):
    s = i * 10
    draw.rectangle((0 + s, 200, 20 + s, 210), fill=ground_color, outline=ground_color_line)
img.save('img/background.png', quality=95)