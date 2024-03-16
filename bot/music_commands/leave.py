# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from .common import check_if_bot_turn


@bot.command(name="leave")
async def leave(ctx: commands.Context):
    if await check_if_bot_turn(ctx) is False:
        return

    await ctx.voice_client.disconnect()
    await reply_user(ctx, "✅ Rời rồi vui chưa :)")
