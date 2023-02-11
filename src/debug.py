import discord
import logging
from discord.ext import commands


from utils import TEST_GUILD, extensions


class DebugCommands(commands.Cog):
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
            await ctx.send(f"Synced commands globally and to guild {TEST_GUILD.id}")
            logging.info("Successful manual sync to Discord")

        except discord.HTTPException:
            logging.error(f"HTTPException while manually syncing commands")

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
                    logging.info(f"Extension {arg} manually reloaded")

                except commands.ExtensionNotLoaded:
                    await ctx.send(f"Extension {arg} was never loaded!")
                    logging.error(
                        f"Existing extension {arg} was never loaded and thus could not be reloaded"
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
