import discord
from discord.ext import commands
import youtube_dl
from replit import db

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    def add_song(url):
        if "songs" in db.keys():
            songs = db["songs"]
            songs.append(url)
            db["songs"] = songs
        else:
            db["songs"] = [url]

    def remove_song():
        songs = db["songs"]
        if len(songs) > 0:
            del songs[0]
            db["songs"] = songs


    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before, after):
        pass

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.guild.change_voice_state(channel=voice_channel, self_mute=False, self_deaf=True)
        else:
            await ctx.voice_client.move_to(voice_channel)
    
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def play(self, ctx, url):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz.")
        else:
            await ctx.message.add_reaction('▶️')

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=False, self_deaf=True)

        if ctx.voice_client.is_playing():
            print('Tocando')
        else:
            print('N tocando nada')
        
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        YDL_OPTIONS = {'format': 'bestaudio'}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.message.add_reaction('⏸️')
        await ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        await ctx.message.add_reaction('⏯')
        await ctx.voice_client.resume()

def setup(client):
    client.add_cog(music(client))