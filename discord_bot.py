from asyncio import tasks
import asyncio
import discord
from discord.ext import commands, tasks
import logging
import requests
from decouple import config
from random import choice
from bs4 import BeautifulSoup
import youtube_dl

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, volume=0.5):
        super().__init__(source, volume)

        # self.data = data

        # self.title = data.get('title')
        # self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable="static/sound/FFmpeg/bin/ffmpeg.exe"))


class TheLastWolfpackAPI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="секретные радиограммы"))

    @commands.command(name='cap_info')
    async def cap_info(self, ctx, cap_name, cap_surname):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com/api/caps/{cap_name + ' ' + cap_surname}")
        data = response.json()['captain']
        await ctx.send(f"TheLastWolfpack ID: {data['id']}. Uboat.net profile link: {data['profile_link']}. Full name: {data['name']}. Additional info: {data['info']}. U-boats under command: {data['boats']}.")
        await ctx.send(data['image'])

    @commands.command(name='rand_cap_info')
    async def rand_cap_info(self, ctx):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com/api/caps")
        data = choice(response.json()['captains'])
        await ctx.send(f"TheLastWolfpack ID: {data['id']}. Uboat.net profile link: {data['profile_link']}. Full name: {data['name']}. Additional info: {data['info']}. U-boats under command: {data['boats']}.")
        response = requests.get(data['image'])
        soup = BeautifulSoup(response.content, 'lxml')
        p = soup.find_all('p')
        try:
            if p[0].text != 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.':
                await ctx.send(data['image'])
        except IndexError:
            await ctx.send(data['image'])

    @commands.command(name='uboat_info')
    async def uboat_info(self, ctx, uboat_num):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com/api/uboats/{uboat_num}")
        data = response.json()['uboat']
        await ctx.send(f"""TheLastWolfpack ID: {data['id']}. Tactical number: {data['tactical_number']}. Ordered: {data['ordered']}. Launched: {data['launched']}. Commissioned: {data['commissioned']}. Commanders: {data['commanders'][1:]}. Career: {data['career']}. Successes: {data['successes']}. Fate: {data['fate']}. Coordinates of loss: {data['coords']}.""")

    @commands.command(name='rand_uboat_info')
    async def rand_uboat_info(self, ctx):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com/api/uboats")
        data = choice(response.json()['uboats'])
        await ctx.send(f"""TheLastWolfpack ID: {data['id']}. Tactical number: {data['tactical_number']}. Ordered: {data['ordered']}. Launched: {data['launched']}. Commissioned: {data['commissioned']}. Commanders: {data['commanders'][1:]}. Career: {data['career']}. Successes: {data['successes']}. Fate: {data['fate']}. Coordinates of loss: {data['coords']}.""")

    @commands.command(name='hist_ref')
    async def hist_ref(self, ctx):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com/api/hist_ref")
        data = response.json()
        await ctx.send(data['text'][:2000])
        await ctx.send(data['text'][2000:4000])
        await ctx.send(data['text'][4000:6000])
        await ctx.send(data['text'][6000:])
        await ctx.send(f"Подлодка VII серии U-96 {data['pics'][0]}")
        await ctx.send(f"Карл Дениц {data['pics'][1]}")
        await ctx.send(f"8 июля 1944 года, Бискайский залив, в 90 милях юго-западнее Бреста. После атаки австралийской летающей лодки 'Сандерленд гибнет' U-243 капитан-лейтенанта Ханса Мёртенса. {data['pics'][2]}")
        await ctx.send(f"Cуда конвоя в Северной Атлантике. {data['pics'][3]}")

    @commands.command(name='uboat_ref')
    async def uboat_types(self, ctx):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com/api/uboat_types")
        data = response.json()
        await ctx.send(data['text'][:2000])
        await ctx.send(data['text'][2000:4000])
        await ctx.send(data['text'][4000:6000])
        await ctx.send(data['text'][6000:8000])
        await ctx.send(data['text'][8000:10000])
        await ctx.send(data['text'][10000:12000])
        await ctx.send(data['text'][12000:])
        await ctx.send(f"Подлодка II серии {data['pics'][0]}")
        await ctx.send(f"Подлодка VII серии {data['pics'][1]}")
        await ctx.send(f"Подлодка IX серии {data['pics'][2]}")
        await ctx.send(f"Подлодка XXI серии {data['pics'][3]}")
        await ctx.send(f"Подлодка 641 проекта (1960) {data['pics'][4]}")
        await ctx.send(f"Подлодка 675 проекта (1960) {data['pics'][5]}")
        await ctx.send(f"USS Clamagore в разных модификациях {data['pics'][6]}")

    @commands.command(name='website')
    async def website(self, ctx):
        embedVar = discord.Embed(title="TheLastWolfack", description="[Главная страница](https://the-last-wolfpack.herokuapp.com/)", color=0x808080)
        embedVar.add_field(name="1.", value="[Историческая справка](https://the-last-wolfpack.herokuapp.com/historical_reference)", inline=False)
        embedVar.add_field(name="2.", value="[Типы лодок Кригсмарине](https://the-last-wolfpack.herokuapp.com/uboat_types)", inline=False)
        embedVar.add_field(name="3.", value="[Подводные лодки Кригсмарине](https://the-last-wolfpack.herokuapp.com/uboats)", inline=False)
        embedVar.add_field(name="4.", value="[Капитаны Кригсмарине](https://the-last-wolfpack.herokuapp.com/captains)", inline=False)
        await ctx.send(embed=embedVar)

    @commands.command(name='join')
    async def join(self, ctx, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(name='play_local')
    async def play_local(self, ctx, query):
        """Plays a file from the local filesystem"""

        source = discord.FFmpegPCMAudio(query, **ffmpeg_options, executable="static/sound/FFmpeg/bin/ffmpeg.exe")
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command(name='play_yt')
    async def play_yt(self, ctx, url):
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        await ctx.send('Now playing!')
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send(
"""```
TheLastWolfpack Bot commands:
  /bdu/help -- показать это сообщение
  /bdu/website -- показать ссылки на разделы сайта
  /bdu/cap_info <cap_name> <cap_surname> -- вывести информацию об определенном капитане Кригсмарине по его имени и фамилии
  /bdu/rand_cap_info -- вывести информацию о случайном капитаны Кригсмарине
  /bdu/uboat_info <uboat_number> (ex.: /bdu/uboat_info U-96) -- вывести информацию об определенной подлодке Кригсмарине по ее тактическому номеру
  /bdu/uboat_info -- вывести информацию о случайной подлодке Кригсмарине
  /bdu/hist_ref -- вывести историческую справку и Битве за Атлантику
  /bdu/uboat_ref -- вывести справку по основным типам подлодок Кригсмарине
  /bdu/join <channel> -- бот подключится к указанному каналу
  /bdu/play_local <path> -- бот воспроизведет указанный аудиофайл
  /bdu/play_yt <url> -- бот воспроизведет звук из видео по ссылке на YouTube
  /bdu/stop -- бот отключится от текущего канала
```""")


def run():
    bot = commands.Bot(command_prefix='/bdu/', intents=intents)
    bot.add_cog(TheLastWolfpackAPI(bot))
    TOKEN = config('DISCORD_TOKEN', default='not found')
    bot.run(TOKEN)
