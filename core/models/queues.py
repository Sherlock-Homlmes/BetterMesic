from typing import List, Any

from beanie import Document


class Queues(Document):
    bot_id: int
    guild_id: int
    voice_channel: int
    queue: List[Any] = []
