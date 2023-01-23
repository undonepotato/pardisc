import discord
import os
import logging
from dotenv import load_dotenv
from rich.logging import RichHandler
from colorama import just_fix_windows_console
from discord.ext import commands
from discord import app_commands

# Environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")

# Logging
just_fix_windows_console()
logging.basicConfig(encoding="utf-8", level=logging.INFO, handlers=[RichHandler()])

# Discord intents and guilds
intents = discord.Intents.default()
TEST_GUILD = discord.Object(id=824481238219620372)

class Pardisc(commands.Bot):
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

bot = Pardisc(command_prefix="/", intents=intents)
        
