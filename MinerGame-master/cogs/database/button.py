import discord


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
        embed = discord.Embed(description=f"左に一マス移動")
        embed.set_image(
            url=f"http://localhost:63342/MinerGame-master/MinerGame-master/cogs/assets/img/playing_left.gif")
        await interaction.response.edit_message(embed=embed)
        self.value = True

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=1)
    async def none1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.green, row=2)
    async def arrow_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description=f"左に一マス移動")
        embed.set_image(
            url=f"http://localhost:63342/MinerGame-master/MinerGame-master/cogs/assets/img/playing_left.gif")
        await interaction.response.edit_message(embed=embed)
        self.value = True

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=2)
    async def none2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.green, row=2)
    async def arrow_right(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description=f"右に一マス移動")
        embed.set_image(
            url=f"http://localhost:63342/MinerGame-master/MinerGame-master/cogs/assets/img/playing_right.gif")
        await interaction.response.edit_message(embed=embed)
        self.value = True

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=3)
    async def none3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
    @discord.ui.button(emoji='⬇️', style=discord.ButtonStyle.green, row=3)
    async def arrow_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description=f"下に一マス移動")
        embed.set_image(
            url=f"http://localhost:63342/MinerGame-master/MinerGame-master/cogs/assets/img/playing_back.gif")
        await interaction.response.edit_message(embed=embed)
        self.value = True

    @discord.ui.button(label=u"\u200b", style=discord.ButtonStyle.grey, row=3)
    async def none4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
