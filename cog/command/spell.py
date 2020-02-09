import aiohttp
import discord
from discord.ext import commands
import random
import re

site = 'http://onestepfromeden.gamepedia.com/Spells'

class spells(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spell(self, ctx, *, spelltext = None):
        if spelltext is None:
            await ctx.send('{ctx.author.mention}, I cannot get a spell for you if you don\'t ask for one...')
            return
        msg = await ctx.send('Querying the OSFE gamepedia, please wait...')
        async with aiohttp.ClientSession() as session:
            async with session.get(site) as read:
                if read.status == 200:
                    html = await read.text()
        html = html.replace('\n','')
        pattern = '<tr><td>(?:.*?)<a href="(?:.*?)" class=(?:"new"(?:.*?)<\/a><\/div>(.*?)<\/div>|"image"(?:.*?)src="(.*?)"(?:.*?)<\/a>)(?:.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><\/tr>'
        thelist = []
        for result in re.findall(pattern, html):
            thelist.append(list(result))
        for x in range(len(thelist)):
            for y in range(len(thelist[x])):
                if thelist[x][y] == '':
                    thelist[x][y] = '\U0000FEFF'
        spellmatch = None
        for x in thelist:
            if spelltext.lower() == x[2].lower() or spelltext.lower() == x[11].lower():
                spellmatch = x

        if spellmatch is None:
            await msg.edit(content=f'{ctx.author.mention}, I cannot find that spell in the wiki...')
            return

        embed = discord.Embed(title=spellmatch[2], description=spellmatch[7])
        if spellmatch[1] != '\U0000FEFF':
            embed.set_thumbnail(url=spellmatch[1])
        embed.add_field(name='Mana', value=spellmatch[3])
        embed.add_field(name='Damage', value=spellmatch[5])
        embed.add_field(name='Shots', value=spellmatch[6])
        embed.add_field(name='ID', value=spellmatch[11])
        embed.add_field(name='Brand', value=spellmatch[9])
        embed.add_field(name='Rarity', value=spellmatch[8])
        embed.add_field(name='Effect', value=spellmatch[4],inline=False)
        embed.set_footer(text=f'Tags:{spellmatch[10]}')
        await msg.edit(content=None,embed=embed)

def setup(bot):
    bot.add_cog(spells(bot))
