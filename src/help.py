"""
Help commands for the bot. NOT for the repository.
"""

import discord
from discord import app_commands
from discord.ext import commands


@commands.guild_only()
class HelpCog(commands.Cog, name="Help Commands"):
    """
    General help commands.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="help", description="How does this work?")
    async def help_command(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(color=discord.Color.green(), title="Welcome to pardisc!")
        embed.description = """
        Hey! I'm a bot that does stuff. There's no setup needed, so you can go ahead and get started with some virtual party games! For example, **Paranoia** is a party game if you're bored with friends. Try doing /paranoia help to learn more!
        """
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelpCog(bot))
