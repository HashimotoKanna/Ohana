import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from aiosqlite import connect
from .database import button, database
import traceback

IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_PATH = f'{IMG_PATH}/background.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'


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
    async def mine(self, ctx, direct=None):
        try:
            Mine = database.Mine(ctx=ctx)
            user_id = ctx.author.id
            fname = "playing_front.png"

            async with connect(DB_PATH) as conn:
                async with conn.cursor() as cur:
                    depth, mine_text, layer = await Mine.player_mine(user_id, 0, 1, conn, cur)
                    depth = (layer-1) * 20 + depth[1]
                    text = f"{mine_text}\n\n現在深度{depth}"

                    embed = discord.Embed(description=text)
                    file = discord.File(fp=IMG_PATH + "/" + fname, spoiler=False)
                    embed.set_image(url=f"attachment://{fname}")
                    view = button.Confirm()
                    await ctx.send(file=file, embed=embed, view=view)
        except:
            return print("エラー情報\n" + traceback.format_exc())

    @commands.command(name='inventory', alias=["inv", "i"])
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def inventory(self, ctx):
        try:
            user_id = ctx.author.id
            async with connect(DB_PATH) as conn:
                async with conn.cursor() as cur:
                    items = await get_player_items(self, user_id, conn, cur)  # プレイヤーの所有しているアイテムをすべて取得

        except:
            return print("エラー情報\n" + traceback.format_exc())

    @commands.command(name='status', aliases=["st"])
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def status(self, ctx):
        embed = discord.Embed()
        embed.set_author(name=self.bot.user,
                         icon_url=self.bot.user.avatar_url
                         )
        await ctx.send("status一覧")


async def get_player_items(self, user_id, conn, cur):
    try:
        await cur.execute("SELECT item_id, count FROM item WHERE user_id=?", (user_id,))
        i_list = ''.join(f'{self.bot.item_lists[i[0]]} : {i[1]}個\n' for i in await cur.fetchall())

    except:
        print("エラー情報\n" + traceback.format_exc())









async def setup(bot: commands.Bot):
    await bot.add_cog(test(bot))
