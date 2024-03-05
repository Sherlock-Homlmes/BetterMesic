# libraries
import discord
from discord.ext import commands
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# env
load_dotenv(dotenv_path=".env")


class Settings(BaseSettings):
    TOKEN: str
    DATABASE_URL: str


settings = Settings()
botname = "Better Mesic"

# bot's def
bot = commands.Bot(
    command_prefix="?", case_insensitive=True, intents=discord.Intents.all()
)
bot.remove_command("help")
