# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from .play import delete_queue


@bot.command(name="stop")
async def stop(ctx: commands.Context):
    await delete_queue(ctx)
    await ctx.voice_client.disconnect()
    await reply_user(ctx, "⏸✅ Chúng ta. Dừng lại ở đây thôi...")
