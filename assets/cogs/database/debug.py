import asyncio
import io
import traceback
import textwrap
import contextlib

from discord.ext import commands
from discord import NotFound, Embed, Forbidden

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


class debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(name='eval', pass_context=True, description="※運営専用コマンド")
    @commands.bot_has_permissions(read_messages=True, send_messages=True, embed_links=True, add_reactions=True,
                                  manage_messages=True, read_message_history=True)
    async def evals(self, ctx):
        try:
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

        except (NotFound, asyncio.TimeoutError, Forbidden):
            return
        except:
            return print("エラー情報\n" + traceback.format_exc())


async def setup(bot):
    await bot.add_cog(debug(bot))
