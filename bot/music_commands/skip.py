# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user


@bot.command(name="skip")
async def skip(ctx: commands.Context):
    ctx.voice_client.stop()
