# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user


@bot.command(name="join")
async def join(ctx: commands.Context):
    destination = ctx.message.author.voice.channel
    if ctx.voice_client is None:
        await reply_user(ctx, "✅ Successfully Joined The VC")
        await destination.connect()
    else:
        await reply_user(ctx, "❎ Error! Bot is already in a VC")
