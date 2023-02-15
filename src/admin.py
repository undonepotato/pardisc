"""
Administration commands for the bot; for example, changing the bot's presence.
"""

import typing
import discord
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

    @commands.dm_only()
    @commands.is_owner()
    @commands.command(name="status")
    async def change_status(
        self,
        ctx: commands.Context,
        status: typing.Literal["online", "idle", "dnd", "invisible"],
        activity_type: typing.Optional[typing.Literal["game", "custom"]],
        activity_text: typing.Optional[str],
    ):

        status_to_change_to = None
        activity = None

        if status == "online":
            status_to_change_to = discord.Status.online
        elif status == "idle":
            status_to_change_to = discord.Status.idle
        elif status == "dnd":
            status_to_change_to = discord.Status.do_not_disturb
        elif status == "invisible":
            status_to_change_to = discord.Status.invisible
        else:
            return await ctx.send(
                "Your `status` argument is wrong! Use either "
                "'online', 'idle', 'dnd', or 'invisible'."
            )

        if (activity_type is None and activity_text is not None) or (
            activity_type is not None and activity_text is None
        ):
            return await ctx.send(
                "If you're adding one of the `activity` parameters, "
                "please add the other one as well."
            )

        if activity_text is not None and len(activity_text) > 99:
            return await ctx.send(
                "Make the `activity_text` parameter under 100 characters, please!"
            )

        if activity_type == "game":
            activity = discord.Game(name=activity_text)
        elif activity_type == "custom":
            activity = discord.CustomActivity(name=activity_text)

        await self.bot.change_presence(activity=activity, status=status_to_change_to)
        await ctx.send("Done!")

    @change_status.error
    async def change_status_error(
        self, ctx, error
    ):  # This is a bit lazy, but I'll be the only one using it. Should be fine..
        await ctx.send(error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotAdmin(bot))
