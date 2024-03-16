# libraries
import asyncio
from typing import Optional
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from core.error_handler import YTDLError
from services.youtube_mesic import YTDLSource, sourceData
from core.models import Queues
from .common import check_if_bot_turn


async def get_current_queue(ctx: commands.Context) -> Queues | None:
    queue = await Queues.find_one(
        Queues.bot_id == bot.user.id,
        Queues.guild_id == ctx.guild.id,
    )
    if queue is None:
        return
    return queue


async def update_or_insert_queue(ctx: commands.Context, source_info: dict):
    source = sourceData(**source_info)
    queue = await get_current_queue(ctx)
    if queue is None:
        queue = await Queues(
            bot_id=bot.user.id,
            guild_id=ctx.guild.id,
            voice_channel=ctx.message.author.voice.channel.id,
            queue=[
                source,
            ],
        ).insert()
    if source not in queue.queue:
        queue.queue.append(source)
        await queue.save()

    return queue


async def get_source_from_source_info(ctx: commands.Context, source_info):
    try:
        return await YTDLSource.create_source(ctx, source_info)
    except YTDLError as e:
        await ctx.send(
            "An error occurred while processing this request: {}".format(str(e))
        )


async def play_song_from_source(ctx: commands.Context, source, send_message: Optional[bool] = True):
    if not ctx.guild.voice_client:
        vc = ctx.message.author.voice.channel
        await vc.connect()
    await ctx.guild.change_voice_state(
        channel=ctx.author.voice.channel, self_deaf=True
    )
    ctx.voice_client.play(source)
    if send_message is True:
        await reply_user(ctx, f"✅ Chơi bài nhạc này nào {str(source)}")


async def play_song_from_queue(ctx: commands.Context):
    queue = await get_current_queue(ctx)
    if queue is None:
        return

    if queue.loop is False and len(queue.queue) == 1:
        await queue.delete()
        await reply_user(ctx, "✅ Mình vừa chơi hết bài rồi đó")
        return None
    else:
        if queue.loop is False:
            queue.queue.pop(0)
            await queue.save()
        source = await get_source_from_source_info(ctx, queue.queue[0])
        if queue.loop is False:
            await play_song_from_source(ctx, source)
        else:
            await play_song_from_source(ctx, source, send_message=True)
        return queue


async def delete_queue(ctx: commands.Context):
    await Queues.find(
        Queues.bot_id == bot.user.id,
        Queues.guild_id == ctx.guild.id,
    ).delete()


@bot.command(name="play")
async def play(ctx: commands.Context, *, search: str = None):
    if await check_if_bot_turn(ctx) is False:
        return

    if search is None:
        await reply_user(ctx, "❎ Lỗi! Hãy chọn 1 bài nhạc cụ thể để tôi chơi nhé hêhê")
    else:
        async with ctx.typing():
            source_info = await YTDLSource.validate_source(
                search,
                loop=bot.loop
            )
            source = await get_source_from_source_info(ctx, source_info)
            # TODO: if queue: reply add song to queue
            queue = await update_or_insert_queue(ctx, source_info)
        if len(queue.queue) == 1:
            await play_song_from_source(ctx, source)
            current_queue = 1
            while current_queue is not None:
                while ctx.voice_client and (
                    ctx.voice_client.is_playing() or
                    ctx.voice_client.is_paused()
                ):
                    await asyncio.sleep(1)
                if not ctx.voice_client.is_paused():
                    current_queue = await play_song_from_queue(ctx)
        else:
            await reply_user(ctx, f"✅ Thêm bài {str(source)} vào hàng chờ nek")
