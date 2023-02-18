"""
Contains the commands and views needed for the Paranoia game to function.
"""

import typing
import random
import discord
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
        """
        Help command for Paranoia.
        """
        embed = discord.Embed(title="Paranoia Rules", color=discord.Color.blurple())
        embed.description = """
        **This game requires 4 people minimum.**
        ~~Sucks that you don't have any friends, doesn't it?~~
        **This bot is in private beta testing. Not all features are representative of what will be in the final release.**
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
            For steps that need talking in a call, just send messages in the channel instead. Easy.
            """,
            inline=True,
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.rename(text_calling_mode="calling_mode")
    @app_commands.command(name="start", description="Start a game of Paranoia!")
    async def paranoia_start(
        self,
        interaction: discord.Interaction,
        text_calling_mode: typing.Literal["Yes", "No"],
        participant1: discord.Member,
        participant2: discord.Member,
        participant3: discord.Member,
        participant4: discord.Member,
        participant5: typing.Optional[discord.Member],
        participant6: typing.Optional[discord.Member],
        participant7: typing.Optional[discord.Member],
        participant8: typing.Optional[discord.Member],
    ) -> None:
        await interaction.response.defer(thinking=True)

        raw_participants = [
            participant1,
            participant2,
            participant3,
            participant4,
            participant5,
            participant6,
            participant7,
            participant8,
        ]

        participants = [
            participant for participant in raw_participants if participant is not None
        ]

        calling_mode = True if text_calling_mode == "Yes" else False
        able_to_see = interaction.channel.members
        seen_participants = set()

        for participant in participants:  # Needs to check for all of these cases
            if participant not in able_to_see:
                return await interaction.followup.send(
                    f"{participant.display_name} doesn't seem "
                    "to be able to see this channel. Make sure all participants can see this "
                    "channel, or move to a different one."
                )

            if participant in seen_participants:
                return await interaction.followup.send(
                    "You can't have the same person in there twice! Try again."
                )

            if participant.id == MY_BOT_ID:
                return await interaction.followup.send(
                    "You included me in the list. I'm honored, but no thank you."
                )

            if participant.bot:
                return await interaction.followup.send(
                    "As much as I'd love for bots to play this game, their questions probably "
                    "wouldn't be the most interesting. Try again."
                )

            seen_participants.add(participant)

        random.shuffle(participants)
        order_embed = discord.Embed(title="Order", color=discord.Color.blurple())
        order_embed.description = (
            f"""
        Here's the order! If you don't like it, cry about it (or redo this command).
        If you're satisfied, you can go ahead and click the button to continue.

        1. <@{participants[0].id}>
        2. <@{participants[1].id}>
        3. <@{participants[2].id}>
        4. <@{participants[3].id}>
        """
            + (f"5. <@{participants[4].id}>\n" if 4 < len(participants) else "")
            + (f"6. <@{participants[5].id}>\n" if 5 < len(participants) else "")
            + (f"7. <@{participants[6].id}>\n" if 6 < len(participants) else "")
            + (f"8. <@{participants[7].id}>\n" if 7 < len(participants) else "")
        )
        await interaction.followup.send(
            embed=order_embed,
            view=ParanoiaStartNextSegmentView(
                participants,
                calling_mode,
                participants[0],
                participants[1],
                interaction.user,
            ),
        )


class ParanoiaStartNextSegmentView(discord.ui.View):
    """
    When a segment of a Paranoia round has been completed,
    this button (inside this view) should be pressed to start the next segment.
    """

    def __init__(
        self,
        participants: list,
        calling_mode: bool,
        asker: discord.Member,
        askee: discord.Member,
        confirmator: discord.Member,
    ) -> None:
        self.participants = participants
        self.calling_mode = calling_mode
        self.asker = asker
        self.askee = askee
        self.confirmator = confirmator
        super().__init__()

    @discord.ui.button(label="Continue", style=discord.ButtonStyle.blurple)
    async def paranoia_continue_round_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        if interaction.user != self.confirmator:
            return await interaction.response.send_message(
                (
                    "You didn't start this game!"
                    if self.asker == self.participants[0]
                    else "You're not the responder!"
                ),
                ephemeral=True,
            )

        await interaction.response.send_message(
            f"Now, <@{self.participants[self.participants.index(self.asker)].id}>, "
            f"DM a question to <@{self.participants[self.participants.index(self.askee)].id}>...",
            view=ParanoiaConfirmQuestionSentView(
                self.participants, self.calling_mode, self.asker, self.askee
            ),
        )
        button.disabled = True
        button.style = discord.ButtonStyle.gray
        await interaction.followup.edit_message(
            message_id=interaction.message.id, view=self
        )


class ParanoiaConfirmQuestionSentView(discord.ui.View):
    """
    A button (inside this view) to confirm
    that the question has been sent from the asker to the askee.
    """

    def __init__(
        self,
        participants: list,
        calling_mode: bool,
        asker: discord.Member,
        askee: discord.Member,
    ) -> None:
        self.participants = participants
        self.calling_mode = calling_mode
        self.asker = asker
        self.askee = askee
        super().__init__()

    @discord.ui.button(label="I DMed the question", style=discord.ButtonStyle.green)
    async def paranoia_confirm_question_sent_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        if interaction.user != self.asker:
            return await interaction.response.send_message(
                "You're not the question asker!", ephemeral=True
            )
        button.disabled = True
        button.style = discord.ButtonStyle.gray
        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"And <@{self.participants[self.participants.index(self.askee)].id}>, "
            "the answer is? (Say it in the call!)"
            if self.calling_mode
            else f"And <@{self.participants[self.participants.index(self.askee)].id}>, "
            "the answer is? (Send it in this channel!)",
            view=ParanoiaConfirmAnswerSentView(
                self.participants, self.calling_mode, self.asker, self.askee
            ),
        )


class ParanoiaConfirmAnswerSentView(discord.ui.View):
    """
    A button (inside this view) to confirm that the answer was sent in the channel
    (when the question was already confirmed to be sent).
    """

    def __init__(
        self,
        participants: list,
        calling_mode: bool,
        asker: discord.Member,
        askee: discord.Member,
    ) -> None:
        self.participants = participants
        self.calling_mode = calling_mode
        self.asker = asker
        self.askee = askee
        super().__init__()

    @discord.ui.button(label="I said the answer", style=discord.ButtonStyle.green)
    async def paranoia_confirm_answer_sent_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        if interaction.user != self.askee:
            return await interaction.response.send_message(
                "You're not the question responder!", ephemeral=True
            )
        else:
            button.disabled = True
            button.style = discord.ButtonStyle.gray
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(
                "Now, flip the coin...",
                view=ParanoiaStartCoinFlipView(
                    self.participants, self.calling_mode, self.asker, self.askee
                ),
            )


class ParanoiaStartCoinFlipView(discord.ui.View):
    """
    A button (inside this view) to start the coin flip.
    To be sent after the question answer confirmation.
    """

    def __init__(
        self,
        participants: list,
        calling_mode: bool,
        asker: discord.Member,
        askee: discord.Member,
    ) -> None:
        self.participants = participants
        self.calling_mode = calling_mode
        self.asker = asker
        self.askee = askee
        super().__init__()

    @discord.ui.button(label="Flip the coin", style=discord.ButtonStyle.green)
    async def paranoia_start_coin_flip_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:

        if interaction.user != self.askee:
            return await interaction.response.send_message(
                "You're not the question responder!", ephemeral=True
            )

        coin_is_heads = random.choice([True, False]) # nosec B311

        button.disabled = True
        button.style = discord.ButtonStyle.gray
        await interaction.response.edit_message(view=self)

        if coin_is_heads is True:
            await interaction.followup.send(
                f"Heads.. <@{self.participants[self.participants.index(self.asker)].id}>, "
                "what was the question? (Say in the call!)"
                if self.calling_mode
                else f"Heads.. <@{self.participants[self.participants.index(self.asker)].id}>, "
                "what was the question? (Send in this channel!)",
                view=ParanoiaConfirmQuestionRevealedView(
                    self.participants, self.calling_mode, self.asker, self.askee
                ),
            )

        elif coin_is_heads is False:
            await interaction.followup.send(
                "Tails.. No one will ever know what the question was.",
                view=ParanoiaConfirmQuestionNotRevealedView(
                    self.participants, self.calling_mode, self.asker, self.askee
                ),
            )


class ParanoiaConfirmQuestionRevealedView(discord.ui.View):
    """
    A button (inside this view) to confirm that the question has been
    said or sent in the public channel after a Heads result on the coin flip.

    Should be the last view (or `ParanoiaConfirmQuestionNotRevealedView`)
    sent in the chain before restarting to `ParanoiaStartNextSegmentView` (which this handles).
    """

    def __init__(
        self,
        participants: list,
        calling_mode: bool,
        asker: discord.Member,
        askee: discord.Member,
    ) -> None:
        self.participants = participants
        self.calling_mode = calling_mode
        self.asker = asker
        self.askee = askee
        super().__init__()

    @discord.ui.button(label="I revealed the question", style=discord.ButtonStyle.green)
    async def paranoia_confirm_question_revealed_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:

        if interaction.user == self.asker:
            button.disabled = True
            button.style = discord.ButtonStyle.gray
            await interaction.response.edit_message(view=self)

            if self.askee != self.participants[-1]:
                await interaction.followup.send(
                    "When you're ready for the next round :arrow_down:",
                    view=ParanoiaStartNextSegmentView(
                        self.participants,
                        self.calling_mode,
                        self.participants[self.participants.index(self.asker) + 1],
                        self.participants[self.participants.index(self.askee) + 1],
                        self.askee,
                    ),
                )
            else:
                await interaction.followup.send(
                    "That's the last round! To play again, do /paranoia start."
                )
        else:
            return await interaction.response.send_message(
                "You're not the asker!", ephemeral=True
            )


class ParanoiaConfirmQuestionNotRevealedView(discord.ui.View):
    """
    A button (inside this view) to confirm that the user is ready to move
    to the next round after a Tails coin flip.

    Should be the last view (or `ParanoiaConfirmQuestionRevealedView`)
    sent in the chain before restarting to `ParanoiaStartNextSegmentView` (which this handles).
    """

    def __init__(
        self,
        participants: list,
        calling_mode: bool,
        asker: discord.Member,
        askee: discord.Member,
    ) -> None:
        self.participants = participants
        self.calling_mode = calling_mode
        self.asker = asker
        self.askee = askee
        super().__init__()

    @discord.ui.button(label="Continue", style=discord.ButtonStyle.green)
    async def paranoia_confirm_question_revealed_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        if interaction.user == self.askee:
            button.disabled = True
            button.style = discord.ButtonStyle.gray
            await interaction.response.edit_message(view=self)

            if self.askee != self.participants[-1]:
                await interaction.followup.send(
                    "When you're ready for the next round :arrow_down:",
                    view=ParanoiaStartNextSegmentView(
                        self.participants,
                        self.calling_mode,
                        self.participants[self.participants.index(self.asker) + 1],
                        self.participants[self.participants.index(self.askee) + 1],
                        self.askee,
                    ),
                )
            else:
                await interaction.followup.send(
                    "That's the last round! To play again, do /paranoia start."
                )

        else:
            return await interaction.response.send_message(
                "You're not the responder!", ephemeral=True
            )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Paranoia(bot))
