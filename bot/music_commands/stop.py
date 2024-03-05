# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user


@bot.command(name="stop")
async def stop(ctx: commands.Context):
    ctx.voice_client.stop()
    await reply_user(ctx, "⏸✅ Stopped the song")
