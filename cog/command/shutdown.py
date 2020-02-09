import discord
from discord.ext import commands

class shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send('Shutting down, goodbye!')
        cmd = open('shutdown.txt', 'w')
        cmd.write('')
        cmd.close()
        await self.bot.logout()
        await self.bot.close()

def setup(bot):
    bot.add_cog(shutdown(bot))
