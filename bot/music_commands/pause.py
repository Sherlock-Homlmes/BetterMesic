# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user


@bot.command(name="pause")
async def pause(ctx: commands.Context):
    ctx.voice_client.pause()
    await reply_user(ctx, "⏸️ Paused!")
