import aiohttp
import discord
from discord.ext import commands
import json
import urllib

site = 'https://onestepfromeden.gamepedia.com/api.php?action=query&list=search&srprop=snippet&format=json&srlimit=5&srsearch='
root = 'https://onestepfromeden.gamepedia.com/'

class search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, *, text = None):
        if text is None:
            await ctx.send('{ctx.author.mention}, I cannot search the wiki for you if you give me nothing to search...')
            return
        
        msg = await ctx.send('Querying the OSFE gamepedia, please wait...')
        async with aiohttp.ClientSession() as session:
            async with session.get(site+urllib.parse.quote(text)) as read:
                if read.status == 200:
                    api = await read.json()

        if len(api["query"]["search"]) == 0:
            await msg.edit(content=f'{ctx.author.mention}, I cannot find that in the wiki...')
            return
        
        embed=discord.Embed(title='OSFE Wiki results',color=0xeeeeee)
        for x in api["query"]["search"]:
            embed.add_field(name=x["title"], value=x["snippet"].replace('<span class=\"searchmatch\">','**').replace('</span>','**')+'\n'+root+urllib.parse.quote(x["title"]), inline=False)
        embed.set_thumbnail(url='http://media.decodedvoid.com/media/smugbot/Wiki.png')
        await msg.edit(content=None,embed=embed)

def setup(bot):
    bot.add_cog(search(bot))
