import discord
from discord.ext import commands
import asyncio
import os
import json


with open(r'./assets/config/setting.json', encoding='utf-8') as fh:
    json_txt = fh.read()
    json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
    token = json.loads(json_txt)['token']
    prefix = json.loads(json_txt)['prefix']

with open(r'./assets/config/items.json', encoding='utf-8') as fh:
    json_txt = fh.read()
    json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
    item_list = json.loads(json_txt)['items']

intents = discord.Intents.all()
only_admin = []
admin_list = [605188331642421272]
sqlite_list = []


class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=prefix, intents=intents)
        self.sqlite_list = kwargs.pop("sqlite_list")
        self.item_list = kwargs.pop("item_list")
    def remove_from_list(self, u_id):
        [self.sqlite_list.remove(m) for m in self.sqlite_list if u_id == m[0]]


bot = MyBot(sqlite_list=sqlite_list, item_list=item_list)


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
    for file in os.listdir('assets/cogs/'):
        if file.endswith('.py'):
            await bot.load_extension(f'assets.cogs.{file[:-3]}')


asyncio.run(load_cogs())
bot.run(token)
