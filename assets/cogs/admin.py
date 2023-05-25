import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from aiosqlite import connect
import asyncio
import io
import traceback
import ast
import textwrap
import os
import contextlib
from discord import NotFound, Embed, Forbidden

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
admin_list = [605188331642421272]


def cleanup_code(content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')


def get_syntax_error(e):
    if e.text is None:
        return f'```py\n{e.__class__.__name__}: {e}\n```'
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


def mention_to_user_id(mention):
    user_id = mention.strip("<@").strip(">")
    if user_id.find("!") != -1:
        user_id = user_id.strip("!")
    return int(user_id)


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    # doesn't work here either
    @app_commands.command()
    async def inadmin(self, interaction: discord.Interaction):
        await interaction.response.send_message("lol check in admin")

    @commands.command(name='eval', pass_context=True, description="※運営専用コマンド")
    async def evals(self, ctx):
        if ctx.author.id not in admin_list:
            return await ctx.send("指定ユーザーのみが使用できます")

        env = {'bot': self.bot, 'ctx': ctx, 'channel': ctx.channel, 'author': ctx.author, 'guild': ctx.guild,
               'message': ctx.message, '_': self._last_result}
        env.update(globals())
        body = cleanup_code(ctx.message.content[6:].lstrip())
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception as _:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception:
                pass
            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(name='cdb')
    async def create_database(self, ctx):
        path = DB_PATH
        if not os.path.exists(path):
            open(path, "w").close()
            async with connect(path) as conn:
                async with conn.cursor() as cur:
                    await conn.commit()
                    # テーブル名:『player』
                    await cur.execute("CREATE TABLE IF NOT EXISTS player(user_id BIGINT(20), exp bigint(20), )")
                    await conn.commit()

                    # テーブル名:『item』 カラム内容： ユーザーID 整数型, アイテムID　整数値, 個数 整数値
                    await cur.execute("CREATE TABLE IF NOT EXISTS item(user_id BIGINT(20), item_id INT, count INT)")
                    await conn.commit()

                    # テーブル名:『ban_user』 カラム内容： ユーザーID 整数型
                    await cur.execute("CREATE TABLE IF NOT EXISTS ban_user(user_id BIGINT(20))")
                    await conn.commit()

                    # テーブル名:『in_mine』
                    await cur.execute(
                        "CREATE TABLE IF NOT EXISTS mine(user_id BIGINT(20), depth INT, place INT,player_mine INT)")
                    await conn.commit()

    @commands.command(name='db')
    async def db(self, ctx):
        f"""
        対応してる命令文は下記の5つです。
        [SELECT, DELETE, INSERT, UPDATE, SHOW]
        f"""
        async with connect(DB_PATH) as conn:
            async with conn.cursor() as cur:
                if ctx.author.id not in admin_list:
                    return await ctx.send("指定ユーザーのみが使用できます")

                msg = await ctx.send(
                    embed=Embed(title=f"接続が完了しました。", description=f"このメッセージの次の発言でそのまま基本命令文を発言してください。"))
                # ここで『select * from player』と打てば全てのユーザーのデータが返ってくる
                msg_react = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                if msg_react.content.split()[0].upper() in ["SELECT", "SHOW"]:
                    await cur.execute(msg_react.content)
                    all_deta = await cur.fetchall()
                    # 全てのデータを10個ごとに分けてページにする
                    select_list = ["\n".join("".join([f"[{r}]\n" for r in all_deta]).split("\n")[i:i + 10]) for i in
                                   range(0, len(all_deta), 10)]
                    if not select_list:  # select_listが存在してない場合。つまり空
                        return await msg.edit(embed=Embed(description=f"内容:\n```None```"))

                    embeds = []
                    for embed in select_list:
                        embeds.append(Embed(description=f"内容:\n```{embed}```"))
                    await msg.edit(
                        content=f"```diff\n1ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                        embed=embeds[0])
                    while True:  # 処理が終わる(return)まで無限ループ
                        try:  # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
                            msg_react = await self.bot.wait_for('message', check=lambda
                                m: m.author == ctx.author and m.content.isdigit() and 0 <= int(m.content) <= len(
                                embeds), timeout=30)
                            # await self.bot.wait_for('message')で返ってくるのは文字列型
                            if msg_react.content == "0":
                                # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                                return await msg.edit(content="‌")
                            await msg.edit(
                                content=f"```diff\n{int(msg_react.content)}ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                                embed=embeds[int(msg_react.content) - 1])
                        except asyncio.TimeoutError:  # wait_forの時間制限を超過した場合
                            # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                            return await msg.edit(content="‌", embed=Embed(title=f"時間切れです..."))

                elif msg_react.content.split()[0].upper() in ["DELETE", "UPDATE"]:
                    await msg.edit(
                        content=f"<@{ctx.author.id}>これでいいの？\nこの変更で大丈夫な場合は『ok』\nキャンセルの場合は『no』と発言してください。",
                        embed=Embed(
                            description=f"{msg_react.content.split()[0].upper()}内容:\n```{msg_react.content}```"))
                    # okかnoの発言を待つ処理。　もっと待つメッセージを絞る場合はlambdaにしてください。現在はokかnoだけしか認識できません。
                    ok_no = await self.bot.wait_for('message', check=lambda
                        m: m.author == ctx.author and m.content.lower() in ["ok", "no"])
                    # await self.bot.wait_for('message')で返ってくるのは文字列型
                    if ok_no.content.lower() == "ok":  # メッセージがokだった場合
                        await cur.execute(msg_react.content)
                        await conn.commit()
                        return await msg.edit(
                            embed=Embed(description=f"入力されたデータを{msg_react.content.split()[0].upper()}しました！"))
                    else:  # メッセージがokではなくnoだった場合
                        return await msg.edit(
                            embed=Embed(description=f"入力されたデータを{msg_react.content.split()[0].upper()}しませんでした！"))

                elif msg_react.content.split()[0].upper() == "INSERT":
                    await msg.edit(
                        content=f"<@{ctx.author.id}>これでいいの？\nこの変更で大丈夫な場合は『ok』\nキャンセルの場合は『no』と発言してください。",
                        embed=Embed(description=f"追加データ内容:\n```{msg_react.content}```"))
                    # okかnoの発言を待つ処理。　もっと待つメッセージを絞る場合はlambdaにしてください。現在はokかnoだけしか認識できません。
                    ok_no = await self.bot.wait_for('message', check=lambda
                        m: m.author == ctx.author and m.content.lower() in ["ok", "no"])
                    # await self.bot.wait_for('message')で返ってくるのは文字列型
                    if ok_no.content.lower() == "ok":  # メッセージがokだった場合
                        await cur.execute(msg_react.content)
                        await conn.commit()
                        return await msg.edit(embed=Embed(description=f"入力されたデータをINSERTしました！"))
                    else:  # メッセージがokではなくnoだった場合
                        return await msg.edit(embed=Embed(description=f"入力されたデータをINSERTしませんでした！"))
                else:
                    return await msg.edit(embed=Embed(
                        description=f"ERROR...これは出力できません。\n設定されている基本命令文は下のやつだけです。\n[SELECT, DELETE, INSERT, UPDATE, SHOW]"))


async def is_safe(code: str) -> bool:
    """
    Check if the given code is safe to execute.
    """
    try:
        node = ast.parse(code)
        for node in ast.walk(node):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
                return False
    except SyntaxError:
        return False
    return True


async def setup(bot: commands.Bot):
    await bot.add_cog(admin(bot))
