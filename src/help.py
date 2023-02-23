"""
Help and information commands for the bot.
"""

from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import START_TIME, BOT_VERSION, CHANGELOG


@commands.guild_only()
class HelpCog(commands.Cog, name="Help Commands"):
    """
    General help and information commands.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="help", description="How does this work?")
    async def help_command(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(color=discord.Color.green(), title="Welcome to pardisc!")
        embed.description = ("Hey! I'm a bot that does stuff. There's no setup needed, "
        "so you can go ahead and get started with some virtual party games! For example, "
        "**Paranoia** is a party game if you're bored with friends. "
        "Try doing /paranoia help to learn more!")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="info", description="Get information like the bot uptime and version."
    )
    async def info_command(self, interaction: discord.Interaction) -> None:
        info_embed = discord.Embed(color=discord.Color.blurple(), title="Information")
        info_embed.add_field(name="Ping", value=f"{str(round(self.bot.latency * 1000))} ms")
        info_embed.add_field(
            name="Uptime (H:M:S)",
            value=(str(datetime.now() - START_TIME).split('.', maxsplit=1)[0]),
        )
        info_embed.add_field(name="Bot Version", value=f"`v{BOT_VERSION}`")
        info_embed.add_field(name="Changelog", value=CHANGELOG)
        await interaction.response.send_message(embed=info_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelpCog(bot))
