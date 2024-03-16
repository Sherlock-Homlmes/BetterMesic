# default
import datetime

# libraries
import discord
import beanie

# local
from .conf import bot, botname
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
    await connect_db()
    # TODO: change delete to autoplay
    await Queues.find(Queues.bot_id == bot.user.id).delete()
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.playing, name="?help"),
    )
    # auto delete queue when bot up | join again


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="__Help Menu__",
        description="Write Something Here!",
        color=discord.Colour.red(),
    )
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{botname}")
    embed.set_author(
        name=f"{botname}",
        icon_url="https://cdn.discordapp.com/attachments/968089547894317066/1004129550030090291/repeat-button_1f501.png",
    )
    embed.add_field(
        name="🎶 • Music Commands",
        value="**Command:** ``?join``\n**Usage:** *Joins a voice channel*\n**Command:** ``?leave``\n**Usage:** *leaves the voice channel*\n**Command:** ``?play`` ``<song name>``\n**Usage:** *Plays a song*\n**Command:** ``?pause``\n**Usage:** *Pauses the currently playing song*\n**Command:** ``?resume``\n**Usage:** *Resumes a currently paused song*\n**Command:** ``?summon``\n**Usage:** *Summons the bot to your voice channel*\n**Command:** ``?stop``\n**Usage:** *Stops playing song and clears the queue*",
        inline=False,
    )
    await ctx.send(embed=embed)
    print("{0.user.name} Is Online!".format(bot))
