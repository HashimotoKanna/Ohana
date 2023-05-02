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

    async def embed_response(self, interaction, x, y):
        user_id = interaction.user.id
        Mine = database.Mine(interaction=interaction)
        fname = f"playing_front.png"
        async with connect(DB_PATH) as conn:
            async with conn.cursor() as cur:
                depth, mine_text, layer = await Mine.player_mine(user_id, x, y, conn, cur)
                depth = (layer - 1) * 20 + depth[1]
                text = f"{mine_text}\n\n現在深度{depth}"

                embed = discord.Embed(description=text)
                file = discord.File(fp=IMG_PATH + "/" + fname, spoiler=False)
                embed.set_image(url=f"attachment://{fname}")
                await interaction.response.send_message(file=file, embed=embed, view=Confirm())

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=1)
    async def none0(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='⬆️', style=discord.ButtonStyle.green, row=1)
    async def arrow_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.embed_response(interaction, 0, -1)

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=1)
    async def none1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.green, row=2)
    async def arrow_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.embed_response(interaction, -1, 0)

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=2)
    async def none2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.green, row=2)
    async def arrow_right(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.embed_response(interaction, 1, 0)

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=3)
    async def none3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='⬇️', style=discord.ButtonStyle.green, row=3)
    async def arrow_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.embed_response(interaction, 0, 1)

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=3)
    async def none4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
