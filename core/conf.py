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
bot_ids = [
    1214218774274773032,
    1218466176082907296,
    1218503068103213086,
    1218506513220370432,
    1218773510269173800,
    1218773937924603906,
    1218774362467864620,
    1218775633363210300,
    1218776111022866474,
]

# bot's def
bot = commands.Bot(
    command_prefix="?", case_insensitive=True, intents=discord.Intents.all()
)
bot.remove_command("help")
