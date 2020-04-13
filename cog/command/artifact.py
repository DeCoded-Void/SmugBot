import aiohttp
import discord
from discord.ext import commands
from difflib import SequenceMatcher
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

        pattern = '<tr><td><(?:.*?)<\/span>(?:.*?)src="(.*?)"(?:.*?)<td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>(.*?)<\/td><\/tr>'

        thelist = []
        for result in re.findall(pattern, html):
          thelist.append(list(result))
        for x in range(len(thelist)):
          for y in range(len(thelist[x])):
            if thelist[x][y] == '':
              thelist[x][y] = '\U0000FEFF'
            thelist[x][y] = thelist[x][y].replace('<i>','*').replace('</i>','*')
            thelist[x][y] = re.sub('(<(.*?)>)','',thelist[x][y])
        
        artifactmatch = None
        for x in thelist:
            if artifacttext.lower() == x[1].lower() or artifacttext.lower() == x[1].lower().replace(' ',''):
                artifactmatch = x

        if artifactmatch is None:
            allnames = []
            for possible in thelist:
                allnames.append(possible[1])
            for x in range(len(allnames)):
                ratio = SequenceMatcher(None, allnames[x].lower(), artifacttext.lower()).ratio()
                ratio = int(ratio*10000)
                allnames[x] = [ratio, allnames[x]]
            allnames.sort()
            allnames.reverse()
            allnames = allnames[:3]
            possiblestr = ''
            for x in allnames:
                possiblestr += f'{x[1]}\n'
            embed = discord.Embed(title='Did you mean?')
            embed.add_field(name='Possible Artifacts', value=possiblestr, inline=True)
            await msg.edit(content=f'{ctx.author.mention}, I cannot find that artifact in the wiki...', embed=embed)
            return

        embed = discord.Embed(title=artifactmatch[1], description=artifactmatch[3])
        if artifactmatch[0] != '\U0000FEFF':
            embed.set_thumbnail(url=artifactmatch[0])
        embed.add_field(name='Rarity', value=artifactmatch[4])
        embed.add_field(name='Description', value=artifactmatch[2],inline=False)
        embed.set_footer(text=f'ID: {artifactmatch[6]} | Tags: {artifactmatch[5]}')
        await msg.edit(content=None,embed=embed)

def setup(bot):
    bot.add_cog(artifacts(bot))
