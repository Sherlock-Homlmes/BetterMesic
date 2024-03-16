from core.conf import bot, settings
from core.event_handler import *
from bot.music_commands import *


bot.run(settings.TOKEN)
# local testing
# import asyncio
# import discord
# from core.conf import commands, settings


# async def start_bot(token: str):
#     bot = commands.Bot(
#         command_prefix="?",
#         case_insensitive=True,
#         intents=discord.Intents.all()
#     )
#     bot.remove_command("help")
#     await bot.start(token)


# async def main():
#     await asyncio.gather(
#         *[start_bot(token) for token in [settings.TOKEN1, settings.TOKEN2,]])

# asyncio.run(main())
