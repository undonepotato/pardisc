"""
Houses the bot development and debugging commands.
"""

import logging
import discord
from discord.ext import commands


from utils import TEST_GUILD, extensions


class DebugCommands(commands.Cog):
    """
    Debugging commands for bot development.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @commands.command(name="sync")
    @commands.dm_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        try:
            ctx.bot.tree.copy_global_to(guild=TEST_GUILD)
            await ctx.bot.tree.sync(guild=TEST_GUILD)
            await ctx.send("Synced commands globally and to guild %s", TEST_GUILD.id)
            logging.info("Successful manual sync to Discord")

        except discord.HTTPException:
            logging.error("HTTPException while manually syncing commands")

    @commands.command(name="reload")
    @commands.dm_only()
    @commands.is_owner()
    async def reload_extensions(self, ctx: commands.Context, *args: str) -> None:
        if args[0] == "all":
            args = extensions

        for arg in args:

            if arg not in extensions:
                await ctx.send(
                    "One or more of your arguments is not a valid extension name!"
                )
                break

            else:

                try:
                    await ctx.bot.reload_extension(arg)
                    await ctx.send(f"Extension {arg} successfully reloaded")
                    logging.info("Extension %s manually reloaded", arg)

                except commands.ExtensionNotLoaded:
                    await ctx.send(f"Extension {arg} was never loaded!")
                    logging.error(
                        "Existing extension %s was never loaded and thus could not be reloaded", arg
                    )
                    break

                except commands.ExtensionNotFound:
                    await ctx.send("Extension not found!")
                    break

        await ctx.send("Command finished execution")

    @commands.command(name="dm_user")
    @commands.dm_only()
    @commands.is_owner()
    async def dm_user(self, ctx: commands.Context, uid: int) -> None:
        try:
            await self.bot.get_user(uid).send("Testing!")
        except AttributeError:
            await ctx.send("Error: AttributeError: this might be you!")
        except discord.HTTPException:
            await ctx.send("Sending the message failed! (discord.HTTPException)")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DebugCommands(bot))
