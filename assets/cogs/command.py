import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
import asyncio
from aiosqlite import connect
from .database import button, mine
from .database.mine import Mine
from .database.shop import Shop
from .database.player import Player
from .database.ImageGenerator import ImageGenerator
import traceback
from ..features.players import item


class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.conn.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    # but it works just fine from here
    @app_commands.command()
    @app_commands.check(predicate=True)
    async def intest(self, interaction: button.discord.Interaction):
        await interaction.response.send_message(
            "all good because it's in the same file"
        )

    @commands.command(name="mine")
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def mine(self, ctx, direct=None):
        try:
            Mine = mine.Mine(ctx=ctx, config=self.bot.config)
            user_id = ctx.author.id
            db_path = self.bot.config.get_db()
            playing_path = self.bot.config.get_playing(user_id)

            async with connect(db_path) as conn:
                async with conn.cursor() as cur:
                    depth, mine_text, layer = await Mine.player_mine(0, 1, conn, cur)
                    depth = (layer - 1) * 20 + depth[1]
                    text = f"{mine_text}\n\n現在深度{depth}"

                    embed = discord.Embed(description=text)
                    file = discord.File(fp=playing_path, spoiler=False)
                    embed.set_image(url=f"attachment://{playing_path}")
                    view = button.Confirm(config=self.bot.config)
                    await ctx.send(file=file, embed=embed, view=view)
        except:
            print(traceback.format_exc())

    @commands.command(name="tp")
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def teleport(self, ctx, x=None, y=None, layer=None):
        user_id = ctx.author.id
        db_path = self.bot.config.get_db()
        playing_path = self.bot.config.get_playing(user_id)

        async with connect(db_path) as conn:
            async with conn.cursor() as cur:
                player = Player(ctx=ctx, config=self.bot.config)
                mine = Mine(ctx=ctx, config=self.bot.config)
                img = ImageGenerator(ctx=ctx, config=self.bot.config)
                warp_points = await player.get_player_warp_point(cur)
                if x and y and layer and (int(x), int(y), int(layer)) in warp_points:
                    x, y, layer = int(x), int(y), int(layer)
                    mines = await mine.get_player_mine(cur, layer)
                    await img.make_terrain((x, y), mines, layer)
                    text = f"ここにテレポートしますか？\n" + f"x:{x}, y:{y}, 階層:{layer}\n"
                    embed = discord.Embed(description=text)
                    file = discord.File(fp=playing_path, spoiler=False)
                    embed.set_image(url=f"attachment://{playing_path}")
                    msg = await ctx.send(file=file, embed=embed)
                    while True:
                        try:
                            msg_react = await self.bot.wait_for(
                                "message",
                                check=lambda m: m.author == ctx.author,
                                timeout=30,
                            )
                            if msg_react.content == "ok":
                                mine_text = await player.move(x, y, layer, cur, conn)
                                text = (
                                    f"{mine_text}\n\n" + f"x:{x}, y:{y}, 階層:{layer}\n"
                                )

                                embed = discord.Embed(description=text)
                                file = discord.File(fp=playing_path, spoiler=False)
                                embed.set_image(url=f"attachment://{playing_path}")
                                await ctx.send(file=file, embed=embed)
                                return
                            elif msg_react.content == "no":
                                return await ctx.send(
                                    embed=discord.Embed(description="テレポートを中止しました")
                                )

                        except asyncio.TimeoutError:
                            return await msg.edit(
                                content="‌", embed=discord.Embed(title=f"時間切れです...")
                            )
                text = f"テレポートしたい場所を選択してください\n"
                contents = []
                pos_list = "".join(
                    f"x:{pos[0]}, y:{pos[1]}, 階層:{pos[2]}\n" for pos in warp_points
                )
                msgs = list(
                    filter(
                        lambda a: a != "",
                        [
                            "\n".join(pos_list.split("\n")[i : i + 25])
                            for i in range(0, len(pos_list), 25)
                        ],
                    )
                )
                embeds = [
                    discord.Embed(
                        description=f"```{i if i else 'どこも掘っていません...'}```"
                    ).set_author(name=f"{ctx.author}のテレポート先:")
                    for i in msgs
                ]
                msg = await ctx.send(
                    content=f"```diff\n1ページ/{len(embeds)}ページ目を表示中\nテレポートしたい場所を選択してください\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                    embed=embeds[0],
                )
                while True:
                    try:
                        msg_react = await self.bot.wait_for(
                            "message",
                            check=lambda m: m.author == ctx.author
                            and m.content.isdigit()
                            and 0 <= int(m.content) <= len(embeds),
                            timeout=30,
                        )
                        if msg_react.content == "0":
                            # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                            return await msg.edit(content="‌")
                        await msg.edit(
                            content=f"```diff\n{int(msg_react.content)}ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                            embed=embeds[int(msg_react.content) - 1],
                        )
                    except asyncio.TimeoutError:
                        return await msg.edit(
                            content="‌", embed=discord.Embed(title=f"時間切れです...")
                        )

    @commands.command(name="inventory", alias=["inv", "i"])
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def inventory(self, ctx):
        user_id = ctx.author.id
        db_path = self.bot.config.get_db()
        async with connect(db_path) as conn:
            async with conn.cursor() as cur:
                items = await item.get_player_items(
                    self, user_id, conn, cur
                )  # プレイヤーの所有しているアイテムをすべて取得

    @commands.command(name="status", aliases=["st"])
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def status(self, ctx):
        embed = discord.Embed()
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        await ctx.send("status一覧")

    @commands.command(name="shop")
    @commands.cooldown(1, 8, type=commands.BucketType.user)
    async def shop(self, ctx, direct=None):
        try:
            shop = Shop(ctx=ctx)
            await shop.shop()

        except:
            print(traceback.format_exc())


async def setup(bot: commands.Bot):
    await bot.add_cog(command(bot))
