# libraries
import asyncio
from typing import Optional
import discord
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from core.error_handler import YTDLError
from services.youtube_mesic import YTDLSource, sourceData
from core.models import Queues
from .common import check_if_bot_turn


AFK_LEAVE_TIME = 120
afk_count = 0


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


async def play_song_from_source(
    ctx: commands.Context, source, send_message: Optional[bool] = True
):
    if ctx.voice_client and ctx.voice_client.channel:
        pass
    elif not ctx.guild.voice_client:
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
            await play_song_from_source(ctx, source, send_message=False)
        return queue


async def delete_queue(ctx: commands.Context):
    await Queues.find(
        Queues.bot_id == bot.user.id,
        Queues.guild_id == ctx.guild.id,
    ).delete()


async def is_any_member_in_voice_channel(ctx: commands.Context):
    global afk_count

    if not ctx.voice_client:
        return False
    # auto leave when no one in voice channel
    if (
        ctx.voice_client
        and len(
            [member for member in ctx.voice_client.channel.members if not member.bot]
        )
        == 0
    ):
        afk_count += 1
        if afk_count >= AFK_LEAVE_TIME:
            await delete_queue(ctx)
            await ctx.voice_client.disconnect()
            return False
    else:
        afk_count = 0

    return True


async def is_afk_for_a_long_time(ctx: commands.Context):
    global afk_count

    if not ctx.voice_client:
        return True
    # auto leave when afk for a long time
    if not ctx.voice_client.is_playing():
        afk_count += 1
        if afk_count >= AFK_LEAVE_TIME:
            if ctx.voice_client:
                await ctx.voice_client.channel.send(
                    "❎ Không có việc j làm thì mình out nha :>"
                )
            await delete_queue(ctx)
            await ctx.voice_client.disconnect()
            return True
    else:
        afk_count = 0

    return False


# @bot.command(
#     name="play",
#     aliases=[
#         "p",
#     ],
# )
# async def play(ctx: commands.Context, *, search: str = None):
#     if await check_if_bot_turn(ctx) is False:
#         return

#     if search is None:
#         await reply_user(ctx, "❎ Lỗi! Hãy chọn 1 bài nhạc cụ thể để tôi chơi nhé hêhê")
#     else:
#         async with ctx.typing():
#             source_info = await YTDLSource.validate_source(search, loop=bot.loop)
#             source = await get_source_from_source_info(ctx, source_info)
#             # TODO: if queue: reply add song to queue
#             queue = await update_or_insert_queue(ctx, source_info)
#         if len(queue.queue) == 1:
#             await play_song_from_source(ctx, source)
#             current_queue = 1
#             while current_queue is not None:
#                 while ctx.voice_client and (
#                     ctx.voice_client.is_playing() or ctx.voice_client.is_paused()
#                 ):
#                     await asyncio.sleep(2)
#                     if not await is_any_member_in_voice_channel(ctx):
#                         current_queue = None
#                         break
#                 if (
#                     await is_any_member_in_voice_channel(ctx)
#                     and not ctx.voice_client.is_paused()
#                 ):
#                     current_queue = await play_song_from_queue(ctx)
#             while not await is_afk_for_a_long_time(ctx):
#                 await asyncio.sleep(1)
#         else:
#             await reply_user(ctx, f"✅ Thêm bài {str(source)} vào hàng chờ nek")


@bot.command(
    name="play",
    aliases=[
        "p",
    ],
)
async def play(ctx: commands.Context, *, search: str = None):
    if await check_if_bot_turn(ctx) is False:
        return

    if search is None:
        await reply_user(ctx, "❎ Lỗi! Hãy chọn 1 bài nhạc cụ thể để tôi chơi nhé hêhê")
    else:
        async with ctx.typing():
            if ctx.voice_client and ctx.voice_client.channel:
                pass
            elif ctx.message.author.voice:
                vc = ctx.message.author.voice.channel
                await vc.connect()
                await ctx.guild.change_voice_state(
                    channel=ctx.author.voice.channel, self_deaf=True
                )
            else:
                await reply_user(ctx, "❎ Bạn cần ở trong một kênh thoại để tôi vào!")
                return

            if ctx.voice_client:
                url = "https://new-files.betterme.study/audios/94bc253b_M_t_L_i_n_-_B_t_Band_Demo_-_Remastered.opus"
                try:
                    source = discord.FFmpegOpusAudio(url)
                    ctx.voice_client.play(
                        source,
                        after=lambda e: print(f"Player error: {e}") if e else None,
                    )
                    await reply_user(ctx, f"✅ Đang phát abc")
                except Exception as e:
                    await reply_user(ctx, f"❎ Lỗi khi phát file local: {str(e)}")
            else:
                await reply_user(ctx, "❎ Không thể kết nối vào kênh thoại.")
