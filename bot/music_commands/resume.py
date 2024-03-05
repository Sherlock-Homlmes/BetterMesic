# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user


@bot.command(name="resume")
async def resume(ctx: commands.Context):
    ctx.voice_client.resume()
    await reply_user(ctx, "⏸️ Resumed!")
