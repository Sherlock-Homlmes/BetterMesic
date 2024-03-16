# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from .play import get_current_queue 
from .common import check_if_bot_turn


@bot.command(name="loop")
async def loop(ctx: commands.Context):
    if await check_if_bot_turn(ctx) is False:
        return

    queue = await get_current_queue(ctx)
    queue.loop = True
    await queue.save()
    await reply_user(ctx, "✅ Ok chơi đi chơi lại nek!!!")
