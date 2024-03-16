# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from .common import check_if_bot_turn


@bot.command(name="pause")
async def pause(ctx: commands.Context):
    if await check_if_bot_turn(ctx) is False:
        return

    ctx.voice_client.pause()
    await reply_user(ctx, "⏸️ Paused!")
