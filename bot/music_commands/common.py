# default
import itertools

# libraries
from discord.ext import commands
from core.general_func import reply_user

# local
from core.conf import bot, bot_ids


async def check_if_bot_turn(ctx: commands.Context) -> bool:
    if ctx.message.author.voice is None:
        return False
    if (
        ctx.voice_client
        and ctx.message.author.voice.channel != ctx.voice_client.channel
    ):
        return False

    channel_bot_ids = [
        member.id for member in ctx.message.author.voice.channel.members if member.bot
    ]

    # true if bot in voice channel
    if bot.user.id in channel_bot_ids:
        return True
    play_bot_id: int = 0

    all_other_music_bot_in_guild = list(
        itertools.chain.from_iterable(
            [
                [
                    member.id
                    for member in channel.members
                    if member.bot and member.id in bot_ids and member.id != bot.user.id
                ]
                for channel in ctx.guild.voice_channels
            ]
        )
    )

    # true if other bot also not in voice channel
    if any(
        bot_id
        for bot_id in bot_ids
        if bot_id in channel_bot_ids and bot_id in all_other_music_bot_in_guild
    ):
        return False

    # true if bot not in voice channel
    for bot_id in bot_ids:
        if bot_id not in channel_bot_ids and bot_id not in all_other_music_bot_in_guild:
            play_bot_id = bot_id
            break

    # out of bot
    if play_bot_id == 0 and bot.user.id == bot_ids[0]:
        await reply_user(ctx, "Hết bot goi :(")
        return False

    if bot.user.id == play_bot_id:
        return True

    # false
    return False
