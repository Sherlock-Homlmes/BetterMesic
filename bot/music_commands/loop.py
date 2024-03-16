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
    message: str
    if queue.loop:
        queue.loop = False
        message = "✅ Ok bỏ chơi lại nek!!!"
    else:
        queue.loop = True
        message = "✅ Ok chơi đi chơi lại nek!!!"
    await queue.save()
    await reply_user(ctx, message)
