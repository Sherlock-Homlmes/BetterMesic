# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from .play import delete_queue
from .common import check_if_bot_turn


@bot.command(name="stop", aliases=["leave",])
async def stop(ctx: commands.Context):
    if await check_if_bot_turn(ctx) is False:
        return

    await delete_queue(ctx)
    await ctx.voice_client.disconnect()
    await reply_user(ctx, "⏸✅ Chúng ta. Dừng lại ở đây thôi...")
