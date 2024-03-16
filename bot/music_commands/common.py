# libraries
from discord.ext import commands

# local
from core.conf import bot, bot_ids


async def check_if_bot_turn(ctx: commands.Context) -> bool:
    if ctx.message.author.voice is None:
        return False
    if ctx.voice_client and ctx.message.author.voice.channel != ctx.voice_client.channel:
        print('not same vc')
        return False

    channel_member_ids = [
        member.id
        for member in ctx.message.author.voice.channel.members
    ]

    # true if bot in voice channel
    if bot.user.id in channel_member_ids:
        return True

    # true if bot not in voice channel and other before bot also not in voice channel
    play_bot_id: int
    for bot_id in bot_ids:
        if bot_id not in channel_member_ids:
            play_bot_id = bot_id
            break
    if bot.user.id == play_bot_id:
        return True

    # false
    return False
