import asyncio
import discord
from discord.ext import commands
import json

class botstatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.loop.create_task(self.status_task())

    async def status_task(self):
        with open('config/playingstatus.json') as f:
            stat = json.load(f)
        while True:
            for stats in stat["status"]:
                if stat["status"][stats] == 'game':
                    activity = discord.Game(name=stats)
                    await self.bot.change_presence(status=discord.Status.online, activity=activity)
                if stat["status"][stats] == 'listening':
                    activity = discord.Activity(type=discord.ActivityType.listening, name=stats)
                    await self.bot.change_presence(status=discord.Status.online, activity=activity)
                if stat["status"][stats] == 'streaming':
                    activity = discord.Streaming(name=stats, url='https://www.twitch.tv/')
                    await self.bot.change_presence(status=discord.Status.online, activity=activity)
                if stat["status"][stats] == 'watching':
                    activity = discord.Activity(type=discord.ActivityType.watching, name=stats)
                    await self.bot.change_presence(status=discord.Status.online, activity=activity)
                await asyncio.sleep(300)

def setup(bot):
    bot.add_cog(botstatus(bot))
