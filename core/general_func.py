# import datetime

import discord
from discord.ext import commands

from .conf import botname


# general funcs
async def reply_user(ctx: commands.Context, description: str) -> None:
    embed = discord.Embed(description=description, colour=discord.Colour.yellow())
    # embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{botname}")
    embed.set_author(
        name=ctx.author.name, icon_url=ctx.author.avatar.url or ctx.author.avatar_url
    )
    await ctx.reply(embed=embed, mention_author=False)
