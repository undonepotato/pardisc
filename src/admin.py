import discord
from discord import app_commands
from discord.ext import commands


class BotAdmin(commands.Cog):
    """
    Global administration commands for the bot. These are all owner-only and DM-only.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @commands.command(name="leave_server")
    @commands.dm_only()
    @commands.is_owner()
    async def leave_server(self, ctx: commands.Context, server_id: int) -> None:
        try:
            await self.bot.get_guild(server_id).leave()
            await ctx.send(
                f"Successfully left guild {self.bot.get_guild(server_id).name} (ID {server_id})"
            )
        except AttributeError:
            await ctx.send("Not a guild that the bot is in, or an invalid ID.")
        except discord.HTTPException:
            await ctx.send("Leaving the guild failed.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotAdmin(bot))
