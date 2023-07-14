import discord
from aiosqlite import connect
from .mine import Mine


class Confirm(discord.ui.View):
    def __init__(self, config=None):
        super().__init__()
        self.value = None
        self.config = config

    async def embed_response(self, interaction, x, y):
        user_id = interaction.user.id
        mine = Mine(interaction=interaction, config=self.config)
        db_path = self.config.get_db()
        playing_path = self.config.get_playing(user_id)
        async with connect(db_path) as conn:
            async with conn.cursor() as cur:
                depth, mine_text, layer = await mine.player_mine(x, y, conn, cur)
                depth = (layer - 1) * 20 + depth[1]
                text = f"{mine_text}\n\n現在深度{depth}"

                embed = discord.Embed(description=text)
                file = discord.File(fp=playing_path, spoiler=False)
                embed.set_image(url=f"attachment://{playing_path}")
                await interaction.response.send_message(
                    file=file, embed=embed, view=Confirm(config=self.config)
                )

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.grey, row=1)
    async def none0(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji="⬆️", style=discord.ButtonStyle.green, row=1)
    async def arrow_up(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.embed_response(interaction, 0, -1)

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.grey, row=1)
    async def none1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.green, row=2)
    async def arrow_left(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.embed_response(interaction, -1, 0)

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.grey, row=2)
    async def none2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.green, row=2)
    async def arrow_right(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.embed_response(interaction, 1, 0)

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.grey, row=3)
    async def none3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji="⬇️", style=discord.ButtonStyle.green, row=3)
    async def arrow_down(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.embed_response(interaction, 0, 1)

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.grey, row=3)
    async def none4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
