# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user


@bot.command(name="leave")
async def leave(ctx: commands.Context):
    if not ctx.guild.voice_client:
        await reply_user(ctx, "❎ Error! Bot is not connected to any VC")
    else:
        await ctx.voice_client.disconnect()
        await reply_user(ctx, "✅ Successfully Left The VC")
