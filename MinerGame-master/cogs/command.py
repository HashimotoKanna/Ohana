import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from aiosqlite import connect
from PIL import Image
from .database import button
import os
import traceback

IMG_PATH = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img'
DB_PATH = 'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/db/mine.db'
BG_PATH = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img/background.png'
NONE_PATH = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img/none.png'
BG_TMP_PATH = f'C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/img/background_tmp.png'

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cog_unload(self):
        self.conn.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    # but it works just fine from here
    @app_commands.command()
    @app_commands.check(predicate=True)
    async def intest(self, interaction: button.discord.Interaction):
        await interaction.response.send_message("all good because it's in the same file")

    @commands.command(name='mine')
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def mine(self, ctx):
        try:
            user_id = ctx.author.id
            async with connect(DB_PATH) as conn:
                async with conn.cursor() as cur:
                    player_depth = await get_player_depth(user_id, conn, cur)  # プレイヤーの深度を取得
                    await mine_(user_id, cur)
                    fname = "playing_front.gif"
                    embed = discord.Embed(description=f"一マス掘りました！\n\n現在深度{player_depth}")
                    embed.set_image(url=f"http://localhost:63342/MinerGame-master/MinerGame-master/cogs/assets/img/playing_front.gif")
                    file = discord.File(fp=IMG_PATH + "/" + fname, spoiler=False)  # ローカル画像からFileオブジェクトを作成
                    embed.set_image(url=f"attachment://{fname}")  # embedに画像を埋め込むときのURLはattachment://ファイル名
                    view = button.Confirm()
                    await ctx.send(file=file, embed=embed, view=view)
        except:
            return print("エラー情報\n" + traceback.format_exc())

    @commands.command(name='status', aliases=["st"])
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def status(self, ctx):
        await ctx.send("status一覧")


async def get_player_depth(user_id, conn, cur):
    try:
        await cur.execute("SELECT depth FROM mine WHERE user_id=?", (user_id,))
        player = await cur.fetchone()
        if not player:
            await cur.execute("INSERT INTO mine values(?,?,?,?)", (user_id, 1, 1, 1))
            await conn.commit()
            return 1
        await cur.execute("UPDATE mine SET depth=? WHERE user_id=?", (player[0] + 1, user_id))
        await conn.commit()
        return player[0] + 1
    except:
        print("エラー情報\n" + traceback.format_exc())


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


async def mine_(user_id, cur):
    try:
        await cur.execute("SELECT depth FROM mine WHERE user_id=?", (user_id,))
        player = await cur.fetchone()
        if player[0] == 1: return
        x = 220
        y = 200
        img = Image.open(NONE_PATH)
        background_img = Image.open(BG_PATH)
        i_x = img.width - 8
        i_y = img.height - 8
        for _ in range(player[0] - 1):
            img = img.resize((i_x, i_y))
            background_img.paste(img, (x, y))
            y += 40
            background_img.save(BG_TMP_PATH, quality=95)

        create_animation("front", x, y)

    except:
        print("エラー情報\n" + traceback.format_exc())


async def setup(bot: commands.Bot):
    await bot.add_cog(test(bot))
