import traceback
from PIL import Image
async def mine_(user_id, cur):
    try:
        await cur.execute("SELECT depth FROM mine WHERE user_id=?", (user_id,))
        player = await cur.fetchone()
        new_img_list = []
        if player[0] == 1:return
        x = 0
        y = 0
        none_name = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img/none.png'
        img = Image.open(none_name)
        bg_name = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img/none.png'
        background_img = Image.open(bg_name)
        for i in range(player[0] - 1):
            img = img.resize(((img.width - 8), (img.height - 8)))
            background_img.paste(img, (220 + x, 200 + y))
            x += 40
            y += 40
            img.save('img/background.png', quality=95)
    except:
        print("エラー情報\n" + traceback.format_exc())

