from asyncio import tasks
import discord
from discord.ext import commands, tasks
import random, logging
import requests

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
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com//api/caps/{cap_name + ' ' + cap_surname}")
        data = response.json()['captain']
        await ctx.send(f"TheLastWolfpack ID: {data['id']}. Uboat.net profile link: {data['profile_link']}. Full name: {data['name']}. Additional info: {data['info']}. U-boats under command: {data['boats']}.")
        await ctx.send(data['image'])

    @commands.command(name='uboat_info')
    async def uboat_info(self, ctx, uboat_num):
        response = requests.get(f"https://the-last-wolfpack.herokuapp.com//api/uboats/{uboat_num}")
        data = response.json()['uboat']
        await ctx.send(f"""TheLastWolfpack ID: {data['id']}. Tactical number: {data['tactical_number']}. Ordered: {data['ordered']}. Launched: {data['launched']}. Commissioned: {data['commissioned']}. Commanders: {data['commanders'][1:]}. Career: {data['career']}. Successes: {data['successes']}. Fate: {data['fate']}. Coordinates of loss: {data['coords']}.""")


bot = commands.Bot(command_prefix='/bdu/', intents=intents)
bot.add_cog(TheLastWolfpackAPI(bot))
TOKEN = "OTU5OTAwMjU1NDQ3NTU2MTM2.Ykimxg.EeJyhXyqKLXSwLirkj0QkvWrxXI"
bot.run(TOKEN)
