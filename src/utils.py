"""
Singletons, such as the bot ID, and setup functions, such as loading extensions.
"""

import os
import logging
from datetime import datetime

import discord
from dotenv import load_dotenv
from rich.logging import RichHandler
from colorama import just_fix_windows_console
from discord.ext import commands


# Environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")

# Logging
just_fix_windows_console()
logging.basicConfig(encoding="utf-8", level=logging.INFO, handlers=[RichHandler()])

# Discord intents, guilds, and extensions
intents = discord.Intents(
    guilds=True,
    members=True,
    bans=False,
    emojis=True,
    integrations=False,
    webhooks=False,
    invites=False,
    voice_states=False,
    presences=False,
    messages=True,
    reactions=True,
    typing=False,
    message_content=False,
    guild_scheduled_events=False,
    auto_moderation=False,
)

TEST_GUILD = discord.Object(id=int(os.getenv("TEST_GUILD")))
MY_BOT_ID = int(os.getenv("BOT_ID"))

extensions = ["debug", "admin", "help", "paranoia"]

# Version information and changelogs
BOT_VERSION = os.getenv("BOT_VERSION")
CHANGELOG = os.getenv("CHANGELOG")
START_TIME = None


class Pardisc(commands.Bot):
    """
    `commands.Bot`, except it loads extensions in `setup_hook`
    and gets the start time in `on_ready`.
    """

    async def setup_hook(self) -> None:
        for extension in extensions:
            await self.load_extension(extension)

    async def on_ready(self) -> None:
        global START_TIME # pylint: disable=global-statement
        START_TIME = datetime.now()


bot = Pardisc(command_prefix="@@", intents=intents)
