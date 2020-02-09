import aiohttp
import discord
from discord.ext import commands
import random
import re

site = 'https://onestepfromeden.gamepedia.com/Artifacts'

class artifacts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def artifact(self, ctx, *, artifacttext = None):
        if artifacttext is None:
            await ctx.send('{ctx.author.mention}, I cannot get an artifact for you if you don\'t ask for one...')
            return
        msg = await ctx.send('Querying the OSFE gamepedia, please wait...')
        async with aiohttp.ClientSession() as session:
            async with session.get(site) as read:
                if read.status == 200:
                    html = await read.text()
        html = html.replace('\n','')
        pattern = '<tr><th><div class="center"><div class="floatnone"><a href="\/File(?:.*?)src="(.*?)"(?:.*?)<\/div><\/div>(.*?)<\/th><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><\/tr>'
        thelist = []
        for result in re.findall(pattern, html):
          thelist.append(list(result))
        for x in range(len(thelist)):
          for y in range(len(thelist[x])):
            if thelist[x][y] == '':
              thelist[x][y] = '\U0000FEFF'
            thelist[x][y] = thelist[x][y].replace('<i>','*').replace('</i>','*')
        artifactmatch = None
        for x in thelist:
            if artifacttext.lower() == x[1].lower() or artifacttext.lower() == x[1].lower().replace(' ',''):
                artifactmatch = x

        if artifactmatch is None:
            await msg.edit(content=f'{ctx.author.mention}, I cannot find that artifact in the wiki...')
            return

        embed = discord.Embed(title=artifactmatch[1], description=artifactmatch[3])
        if artifactmatch[0] != '\U0000FEFF':
            embed.set_thumbnail(url=artifactmatch[0])
        embed.add_field(name='Rarity', value=artifactmatch[4])
        embed.add_field(name='Effect', value=artifactmatch[2],inline=False)
        embed.set_footer(text=f'Tags: {artifactmatch[5]}')
        await msg.edit(content=None,embed=embed)

def setup(bot):
    bot.add_cog(artifacts(bot))
