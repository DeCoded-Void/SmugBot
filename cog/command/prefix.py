import discord
from discord.ext import commands
import json

with open('config/config.json') as cfg:
    config = json.load(cfg)
defaultprefix = config["default_prefix"]

class prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def prefix(self, ctx, *, new_prefix: str = defaultprefix):
        if len(new_prefix) > 15:
            await ctx.send('Why even have a prefix that long?\nPlease use one < 15 characters.')
            return
        serverdir = 'resource/server/'
        serverid = str(ctx.guild.id)
        serverpath = serverdir+serverid
        prefixpath = serverpath+'/prefix.json'
        with open(prefixpath) as prefixfile:
            prefixes = json.load(prefixfile)
        prefixes["prefix"] =  new_prefix
        with open(prefixpath, 'w') as prefixfile:
            prefixes = json.dump(prefixes, prefixfile)
        await ctx.send(f'Prefix successfully changed to `{new_prefix}`')

def setup(bot):
    bot.add_cog(prefix(bot))
