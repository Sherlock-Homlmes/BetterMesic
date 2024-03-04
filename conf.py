# default
import datetime

# libraries
import discord
from discord.ext import commands
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# env
load_dotenv(dotenv_path=".env")


class Settings(BaseSettings):
    TOKEN: str


settings = Settings()

# bot's def
bot = commands.Bot(
    command_prefix='?',
    case_insensitive=True,
    intents=discord.Intents.all()
)
bot.remove_command('help')
botname = 'Better Mesic'


# general funcs
async def reply_user(ctx: commands.Context, description: str) -> None:
    embed = discord.Embed(
        description='✅ Successfully Joined The VC',
        colour=discord.Colour.red()
    )
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f'{botname}')
    embed.set_author(
        name=ctx.author.name,
        icon_url=ctx.author.avatar.url or ctx.author.avatar_url
    )
    await ctx.reply(
        embed=embed,
        mention_author=False
    )


# error handler
class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name='?help'))
    print('{0.user.name} Is Online!'.format(bot))


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='__Help Menu__',
        description='Write Something Here!',
        color=discord.Colour.red())
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f'{botname}')
    embed.set_author(
        name=f'{botname}',
        icon_url='https://cdn.discordapp.com/attachments/968089547894317066/1004129550030090291/repeat-button_1f501.png'
    )
    embed.add_field(
        name='🎶 • Music Commands',
        value='**Command:** ``?join``\n**Usage:** *Joins a voice channel*\n**Command:** ``?leave``\n**Usage:** *leaves the voice channel*\n**Command:** ``?play`` ``<song name>``\n**Usage:** *Plays a song*\n**Command:** ``?pause``\n**Usage:** *Pauses the currently playing song*\n**Command:** ``?resume``\n**Usage:** *Resumes a currently paused song*\n**Command:** ``?summon``\n**Usage:** *Summons the bot to your voice channel*\n**Command:** ``?stop``\n**Usage:** *Stops playing song and clears the queue*', inline=False)
    await ctx.send(embed=embed)
