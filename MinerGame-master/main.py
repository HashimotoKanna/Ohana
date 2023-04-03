import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from aiosqlite import connect
import ast
import contextlib
import io
import os
import textwrap
import traceback

token = "Njg0MDc0MzMxMDM4NTQ4MDU0.GQL-Tn.WFEv6tAB1cCZ9MS7YcwPPL_1vk9kEdczsae6Ic"
prefix = "ww"
intents = discord.Intents.all()
only_admin = []
admin_list = [605188331642421272]
sqlite_list = []
# 下のやつをpathだと思って使ったらエラー出たわ
DB_PATH = os.environ.get('C:/Users/it0_s/PycharmProjects/MinerGame-master/MinerGame-master/cogs/assets/db/mine.db')


class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=prefix, intents=intents)
        self.sqlite_list = kwargs.pop("sqlite_list")

    def remove_from_list(self, u_id):
        [self.sqlite_list.remove(m) for m in self.sqlite_list if u_id == m[0]]


bot = MyBot(sqlite_list=sqlite_list)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandOnCooldown):
        time = int(err.retry_after)
        msg = await ctx.send(f"あと{time}秒後に使用可能です！")
        await asyncio.sleep(time)
        return await msg.delete()


async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')


asyncio.run(load_cogs())
bot.run(token)
