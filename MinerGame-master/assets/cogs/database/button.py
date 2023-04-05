import discord
from . import database
from aiosqlite import connect
IMG_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/img"
DB_PATH = "C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/assets/db/mine.db"
BG_PATH = f'{IMG_PATH}/background.png'
NONE_PATH = f'{IMG_PATH}/none.png'
BG_TMP_PATH = f'{IMG_PATH}/background_tmp.png'


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=1)
    async def none0(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='⬆️', style=discord.ButtonStyle.green, row=1)
    async def arrow_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        async with connect(DB_PATH) as conn:
            async with conn.cursor() as cur:
                player_depth = await database.player_mine(user_id, 0, 1, conn, cur)  # プレイヤーの深度を取得
                await database.mine_(user_id, cur)
                fname = "playing_front.gif"
                embed = discord.Embed(description=f"一マス掘りました！\n\n現在深度{player_depth}")
                file = discord.File(fp=IMG_PATH + "/" + fname, spoiler=False)  # ローカル画像からFileオブジェクトを作成
                embed.set_image(url=f"attachment://{fname}")
                await interaction.response.send_message(file=file, embed=embed)

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=1)
    async def none1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.green, row=2)
    async def arrow_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        async with connect(DB_PATH) as conn:
            async with conn.cursor() as cur:
                player_depth = await database.player_mine(user_id, -1, 0, conn, cur)  # プレイヤーの深度を取得
                await database.mine_(user_id, cur)
                fname = "playing_front.gif"
                embed = discord.Embed(description=f"一マス掘りました！\n\n現在深度{player_depth}")
                file = discord.File(fp=IMG_PATH + "/" + fname, spoiler=False)  # ローカル画像からFileオブジェクトを作成
                embed.set_image(url=f"attachment://{fname}")
                await interaction.response.send_message(file=file, embed=embed)

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=2)
    async def none2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.green, row=2)
    async def arrow_right(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        async with connect(DB_PATH) as conn:
            async with conn.cursor() as cur:
                player_depth = await database.player_mine(user_id, 1, 0, conn, cur)  # プレイヤーの深度を取得
                await database.mine_(user_id, cur)
                fname = "playing_front.gif"
                embed = discord.Embed(description=f"一マス掘りました！\n\n現在深度{player_depth}")
                file = discord.File(fp=IMG_PATH + "/" + fname, spoiler=False)  # ローカル画像からFileオブジェクトを作成
                embed.set_image(url=f"attachment://{fname}")
                await interaction.response.send_message(file=file, embed=embed)

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=3)
    async def none3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='⬇️', style=discord.ButtonStyle.green, row=3)
    async def arrow_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        async with connect(DB_PATH) as conn:
            async with conn.cursor() as cur:
                player_depth = await database.player_mine(user_id, 0, -1, conn, cur)  # プレイヤーの深度を取得
                await database.mine_(user_id, cur)
                fname = "playing_front.gif"
                embed = discord.Embed(description=f"一マス掘りました！\n\n現在深度{player_depth}")
                file = discord.File(fp=IMG_PATH + "/" + fname, spoiler=False)  # ローカル画像からFileオブジェクトを作成
                embed.set_image(url=f"attachment://{fname}")
                await interaction.response.send_message(file=file, embed=embed)

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=3)
    async def none4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
