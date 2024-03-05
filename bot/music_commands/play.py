# libraries
from discord.ext import commands

# local
from core.conf import bot
from core.general_func import reply_user
from core.error_handler import YTDLError
from services.youtube_mesic import YTDLSource
from core.models import Queues


async def update_or_insert_queue(ctx: commands.Context, source: str):
    print(
        bot.user.id,
        ctx.guild.id,
        ctx.message.author.voice.channel.id,
        [
            source,
        ],
    )
    queue = await Queues.find_one(
        Queues.bot_id == bot.user.id,
        Queues.guild_id == ctx.guild.id,
    )
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


@bot.command(name="play")
async def play(ctx: commands.Context, *, search: str = None):
    if search is None:
        await reply_user(ctx, "❎ Error! Please specify a song to play")
    else:
        async with ctx.typing():
            source_info = await YTDLSource.validate_source(search, loop=bot.loop)
            # TODO: if queue: reply add song to queue
            queue = await update_or_insert_queue(ctx, source_info)
            try:
                source = await YTDLSource.create_source(ctx, source_info)
            except YTDLError as e:
                await ctx.send(
                    "An error occurred while processing this request: {}".format(str(e))
                )
            else:
                if not ctx.guild.voice_client:
                    vc = ctx.message.author.voice.channel
                    await vc.connect()
                await ctx.guild.change_voice_state(
                    channel=ctx.author.voice.channel, self_deaf=True
                )
                ctx.voice_client.play(source)
                await reply_user(ctx, f"✅ Enqueued {str(source)}")
