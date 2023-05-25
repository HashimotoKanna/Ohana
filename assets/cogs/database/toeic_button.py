import discord
import random
import json


def get_path():
    with open('assets/config/paths.json', encoding='utf-8') as fh:
        json_txt = fh.read()
        json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
        paths_list = json.loads(json_txt)
        return paths_list


paths_list = get_path()

IMG_PATH = paths_list["ABS_PATH"] + paths_list["IMG_PATH"]
DB_PATH = paths_list["ABS_PATH"] + paths_list["DB_PATH"]
BG_PATH = paths_list["IMG_PATH"] + paths_list["BG_PATH"]
NONE_PATH = paths_list["IMG_PATH"] + paths_list["NONE_PATH"]
BG_TMP_PATH = paths_list["IMG_PATH"] + paths_list["BG_TMP_PATH"]
TREASURE_BOX_PATH = paths_list["IMG_PATH"] + "treasure_box.png"
SHOP_PATH = paths_list["IMG_PATH"] + "shop.png"


class Toeic_button(discord.ui.View):
    def __init__(self, question, answer, not_answer1, not_answer2):
        super().__init__()
        self.value = None
        self.question = question
        self.answer = answer
        self.not_answer1 = not_answer1
        self.not_answer2 = not_answer2
        self.ans_list = [self.answer, self.not_answer1, self.not_answer2]
        random.shuffle(self.ans_list)

    async def embed_response(self, interaction, question, answer):
        user_id = interaction.user.id

        depth, mine_text, layer = await mine.player_mine(x, y, conn, cur)
        depth = (layer - 1) * 20 + depth[1]
        text = f"**{question}**\n\n正しい意味はどれ？"

        embed = discord.Embed(description=text)
        file = discord.File(fp=IMG_PATH + "/" + fname, spoiler=False)
        embed.set_image(url=f"attachment://{fname}")
        await interaction.response.send_message(file=file, embed=embed, view=Confirm())

    @discord.ui.button(emoji="1⃣", style=discord.ButtonStyle.grey, row=1)
    async def none0(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True

    @discord.ui.button(emoji='2⃣', style=discord.ButtonStyle.green, row=1)
    async def arrow_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.embed_response(interaction, 0, -1)

    @discord.ui.button(emoji="3⃣", style=discord.ButtonStyle.grey, row=1)
    async def none1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
