import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore


# custom error type
class CheckFailedLol(app_commands.CheckFailure):
    def __init__(self, lol_id: int, bot: commands.Bot):
        self.lol_id = lol_id
        self.bot = bot
        super().__init__(f"Failed to LOL (user) for {lol_id} ({bot.get_user(lol_id)!r})")


class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    # custom error check decorators for commands
    @staticmethod
    def lol_check(lol_id: int):
        async def predicate(interaction: discord.Interaction) -> bool:
            if interaction.user.id != lol_id:
                raise CheckFailedLol(lol_id, interaction.client)
            return True

        return app_commands.check(predicate)

    # error classification
    @staticmethod
    async def on_tree_error(interaction: discord.Interaction, error: Exception):
        print("on_tree_error called", interaction, error)
        if isinstance(error, CheckFailedLol):
            await interaction.response.send_message(str(error))
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(errors(bot))
    bot.tree.on_error = errors.on_tree_error
