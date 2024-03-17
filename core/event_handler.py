# default
import datetime

# libraries
import discord
import beanie

# local
from .conf import bot, botname, bot_ids
from core.database.mongodb import client
from core.models import document_models, Queues


async def connect_db() -> None:
    print("Connecting to database...")
    await beanie.init_beanie(
        database=client.better_mesic,
        document_models=document_models,
    )
    print("Connect to database success")


@bot.event
async def on_ready():
    print(f"Login as ${bot.user.name}")
    await connect_db()
    # TODO: change delete to autoplay
    await Queues.find(Queues.bot_id == bot.user.id).delete()
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.playing, name="?help"),
    )


@bot.command()
async def help(ctx):
    if bot.user.id != bot_ids[0]:
        return

    embed = discord.Embed(
        title="Lệnh nè 2 ơi",
        description="Tự nhìn dùm nha",
        color=discord.Colour.yellow(),
    )
    # embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{botname}")
    embed.set_author(
        name=f"{botname}",
        icon_url="https://cdn.discordapp.com/attachments/968089547894317066/1004129550030090291/repeat-button_1f501.png",
    )
    embed.add_field(
        name="🎶 • Music Commands",
        value="""**Command:** ``?join``
**Usage:** *Vào chơi cho vui nè*
**Command:** ``?stop``|``?leave``
**Usage:** *Nghỉ chơi nè*
**Command:** ``?play``|``?p`` ``<tên bài hát|link youtube|link soundcloud>``
**Usage:** *Chơi nhạc nè*
**Command:** ``?skip``
**Usage:** *Qua bài tiếp nè*
**Command:** ``?pause``
**Usage:** *Dừng lại nè*
**Command:** ``?resume``
**Usage:** *Tiếp tục nè*
**Command:** ``?loop``
**Usage:** *Chơi đi chơi lại nè*
""",
        inline=False,
    )
    await ctx.send(embed=embed)
    print("{0.user.name} Is Online!".format(bot))
