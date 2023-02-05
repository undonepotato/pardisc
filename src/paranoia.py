import discord
import typing
import random
from types import NoneType
from discord import app_commands
from discord.ext import commands

from utils import MY_BOT_ID

class Paranoia(commands.GroupCog):
    """
    App command group and cog for the Paranoia game.
    """

    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="help", description="What's Paranoia?")
    async def paranoia_help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="Paranoia Rules", color=discord.Color.blurple())
        embed.description = """
        **This game requires 4 people minimum.**
        ~~Sucks that you don't have any friends, doesn't it?~~
        Here's the instructions!
        """
        embed.add_field(
            name="Instructions",
            value="""
            1. Everyone participating gets in a call together.

            2. Everyone sits in a circle. Or rather, I assign a order to the group, since I'm assuming you're *not* in the same place.
            
            3. The first person DMs a question to the second person. The best questions have people at the answers, especially the ones participating.
            
            4. The second person answers the question **out loud, in the call. No one else should know the question other than the first and second people.**
            
            5. I flip a coin for you in a public channel.
            
            6. If that coin is heads, then person 1 says the question out loud to the call.
            
            7. If it's tails, don't tell them - your friends are made to wonder what the question was for the rest of eternity.
            
            8. Keep going until it gets boring. Note that the order is randomized again every time we get through the list of people for variety.
            """,
            inline=True,
        )

        embed.add_field(
            name="No Calling",
            value="""
            0. Unless the number is listed, it's the same as calling mode.
            1. No calling in a no-calling mode.
            4. The second person DMs the answer of the question to me, and I send it in an embed to the public chat.
            6. Same setup as 4. DM to me, I send the embed.
            """,
            inline=True,
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="start", description="Start a game of Paranoia!")
    async def paranoia_start(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        calling_mode: bool,
        participant1: discord.Member,
        participant2: discord.Member,
        participant3: discord.Member,
        participant4: discord.Member,
        participant5: typing.Optional[discord.Member],
        participant6: typing.Optional[discord.Member],
        participant7: typing.Optional[discord.Member],
        participant8: typing.Optional[discord.Member],
    ):
        await interaction.response.defer(thinking=True)

        raw_participants = [
            participant1,
            participant2,
            participant3,
            participant4,
            participant5,
            participant6,
            participant7,
            participant8
        ]

        participants = [participant for participant in raw_participants if participant is not None]

        able_to_see = channel.members
        seen_participants = set()

        for participant in participants: # Needs to check for all of these, so no elifs.
            if participant not in able_to_see:
                return await interaction.followup.send(
                    f"{participant.display_name} doesn't seem to be able to see this channel. Make sure all participants can see this channel or move to a different one."
                )
            
            if participant in seen_participants:
                return await interaction.followup.send("You can't have the same person in there twice! Try again.")

            if participant.id == MY_BOT_ID:
                return await interaction.followup.send("You included me in the list. I'm honored, but no thank you.")

            if participant.bot:
                return await interaction.followup.send("As much as I'd love for bots to play this game, their questions probably wouldn't be the most interesting. Try again.")

            seen_participants.add(participant)
        
        random.shuffle(participants)
        order_embed = discord.Embed(title="Order", color=discord.Color.blurple())
        order_embed.description = f"""
        Here's the order! If you don't like it, cry about it (or redo this command).
        If you're satisfied, you can go ahead and click the button to continue.

        1. <@{participants[0].id}>
        2. <@{participants[1].id}>
        3. <@{participants[2].id}>
        4. <@{participants[3].id}>
        """ + (f"5. <@{participants[4].id}>\n" if 4 < len(participants) else "") + (f"6. <@{participants[5].id}>\n" if 5 < len(participants) else "") + (f"7. <@{participants[6].id}>\n" if 6 < len(participants) else "") + (f"8. <@{participants[7].id}>\n" if 7 < len(participants) else "")
        # debug_embed = discord.Embed(title="Debug", color=discord.Color.blurple())
        # debug_embed.description = f"```py\n{participants}```"
        await interaction.followup.send(embed=order_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Paranoia(bot))
