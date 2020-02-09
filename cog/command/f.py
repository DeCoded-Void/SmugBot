import discord
from discord.ext import commands
import json
import os
import time

counterpath = 'resource/f/F.json'
serverdir = 'resource/server/'

class FCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def counterup(self):
        with open(counterpath) as file:
            data = json.load(file)
        num = float(data["counter"])
        sum = num + 1
        data["counter"] = int(sum)
        with open(counterpath, 'w') as file:
            json.dump(data, file)
        with open(counterpath) as file:
            data = json.load(file)
        return data["counter"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.bot == self.bot.user:
            return

        if 'F' is message.content or 'f' is message.content or message.content == '\U0001F1EB':
            # A dirty and temporary cooldown method
            serverpath = serverdir+str(message.guild.id)
            if not os.path.exists(serverpath):
                os.makedirs(serverpath)
            if not os.path.exists(serverpath+'/f_cooldown.json'):
                with open(serverpath+'/f_cooldown.json', 'w') as f:
                    json.dump({str(message.guild.id):str(int(time.time()))}, f)
            with open(serverpath+'/f_cooldown.json') as f:
                file = json.load(f)
            if int(time.time()) - int(file[str(message.guild.id)]) < 2:
                return

            number = await self.counterup()
            await message.channel.send(f'{number} users have paid their respects...')

            file[str(message.guild.id)] = str(int(time.time()))
            with open(serverpath+'/f_cooldown.json', 'w') as f:
                json.dump(file, f)

    @commands.cooldown(3, 10, commands.BucketType.guild)
    @commands.command()
    async def rip(self, ctx):
        number = await self.counterup()
        await ctx.channel.send(f'{number} users have paid their respects...')

def setup(bot):
    bot.add_cog(FCmd(bot))
