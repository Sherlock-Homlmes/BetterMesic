# libraries
import motor.motor_asyncio

# local
from core.conf import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
