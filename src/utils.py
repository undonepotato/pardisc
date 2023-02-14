"""
Singletons, such as the bot ID, and setup functions, such as loading extensions.
"""

import os
import logging
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

TEST_GUILD = discord.Object(id=1074513568923394108)
MY_BOT_ID = 1067220252594798595
extensions = ["debug", "admin", "help", "paranoia"]


class Pardisc(commands.Bot):
    """
    `commands.Bot`, except it loads extensions in `setup_hook`.
    """
    async def setup_hook(self) -> None:
        for extension in extensions:
            await self.load_extension(extension)


bot = Pardisc(command_prefix="@@", intents=intents)
