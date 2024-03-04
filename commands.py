# libraries
from discord.ext import commands

# local
from conf import bot, reply_user, YTDLError
from youtube_mesic import YTDLSource


###################
@bot.command(name='join')
async def join(ctx: commands.Context):
    destination = ctx.message.author.voice.channel
    if ctx.voice_client is None:
        await reply_user(ctx, '✅ Successfully Joined The VC')
        await destination.connect()
    else:
        await reply_user(ctx, '❎ Error! Bot is already in a VC')


@bot.command(name='leave')
async def leave(ctx: commands.Context):
    if not ctx.guild.voice_client:
        await reply_user(ctx,'❎ Error! Bot is not connected to any VC')
    else:
        await ctx.voice_client.disconnect()
        await reply_user(ctx,'✅ Successfully Left The VC')


@bot.command(name='play')
async def play(ctx: commands.Context, *, search: str = None):
    if search is None:
        await reply_user(ctx, '❎ Error! Please specify a song to play')
    else:
        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                if not ctx.guild.voice_client:
                    vc = ctx.message.author.voice.channel
                    await vc.connect()
                # song = Song(source)
                # await ctx.voice_state.songs.put(song)
                await ctx.guild.change_voice_state(
                    channel=ctx.author.voice.channel,
                    self_deaf=True
                )
                ctx.voice_client.play(source)
                await reply_user(ctx, f'✅ Enqueued {str(source)}')


@bot.command(name='pause')
async def pause(ctx: commands.Context):
    ctx.voice_client.pause()
    await reply_user(ctx, '⏸️ Paused!')


@bot.command(name='resume')
async def resume(ctx: commands.Context):
    ctx.voice_client.resume()
    await reply_user(ctx, '⏸️ Resumed!')


@bot.command(name='stop')
async def stop(ctx: commands.Context):
    ctx.voice_client.stop()
    await reply_user(ctx, '⏸✅ Stopped the song')