from asyncio import tasks
import discord
from discord.ext import commands, tasks
import random, logging
import requests
from decouple import config

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


class TheLastWolfpackAPI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="секретные радиограммы"))

    @commands.command(name='cap_info')
    async def cap_info(self, ctx, cap_name, cap_surname):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com/api/caps/{cap_name + ' ' + cap_surname}")
        data = response.json()['captain']
        await ctx.send(f"TheLastWolfpack ID: {data['id']}. Uboat.net profile link: {data['profile_link']}. Full name: {data['name']}. Additional info: {data['info']}. U-boats under command: {data['boats']}.")
        await ctx.send(data['image'])

    @commands.command(name='uboat_info')
    async def uboat_info(self, ctx, uboat_num):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com/api/uboats/{uboat_num}")
        data = response.json()['uboat']
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


bot = commands.Bot(command_prefix='/bdu/', intents=intents)
bot.add_cog(TheLastWolfpackAPI(bot))
TOKEN = config('DISCORD_TOKEN', default='not found')
bot.run(TOKEN)
