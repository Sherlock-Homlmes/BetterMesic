# default
import asyncio

# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from .common import check_if_bot_turn
from .play import AFK_LEAVE_TIME


@bot.command(name="join")
async def join(ctx: commands.Context):
    is_bot_turn = await check_if_bot_turn(ctx)
    if not is_bot_turn:
        return

    destination = ctx.message.author.voice.channel
    if ctx.voice_client is None:
        await reply_user(ctx, "✅ Vào rồi vui chưa?")
        await destination.connect()
    else:
        await reply_user(ctx, "❎ Đang kênh khác rồi 2 ơi")

    await asyncio.sleep(AFK_LEAVE_TIME)
    if ctx.voice_client and not ctx.voice_client.is_playing():
        await ctx.voice_client.disconnect()