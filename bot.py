import discord
from discord.ext import commands
import json
import os
import sys
import traceback

with open('config/config.json') as cfg:
    config = json.load(cfg)

defaultprefix = config["default_prefix"]
serverdir = 'resource/server/'

def prefix(bot, message):
    if message.guild:
        serverpath = serverdir+str(message.guild.id)
        prefixpath = serverpath+'/prefix.json'
        if not os.path.exists(serverpath):
            os.makedirs(serverpath)
        try:
            with open(prefixpath) as prefixfile:
                prefixes = json.load(prefixfile)
        except Exception as error:
            with open(prefixpath, 'w') as prefixfile:
                json.dump({"prefix":defaultprefix}, prefixfile)
            with open(prefixpath) as prefixfile:
                prefixes = json.load(prefixfile)
    try:
        currentprefix = prefixes["prefix"]
    except Exception as error:
        currentprefix = defaultprefix
    return currentprefix

bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
bot.remove_command('help')

coglist = []
for root, dirs, files in os.walk('cog'):
    for file in files:
        if file.endswith('.py'):
            coglist.append(os.path.join(root, file).replace('\\','.').replace('.py', ''))

if __name__ == '__main__':
    for extension in coglist:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'Failed to load {extension} extension:\n{error}\n\n')

@bot.event
async def on_ready():
    print ('-----The Bot is now online-----')
    print (f'My name is: {bot.user.name}#{bot.user.discriminator}')
    print (f'With the ID: {bot.user.id}')
    print ('Invite me with this link:')
    print (f'https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=0')

@bot.command()
@commands.is_owner()
async def load(ctx, *, cog: str):
    try:
        bot.load_extension(cog)
    except Exception as error:
        await ctx.send(f'**ERROR:** {error}')
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return
    await ctx.send(f'Successfully loaded: `{cog}`')

@bot.command()
@commands.is_owner()
async def unload(ctx, *, cog: str):
    try:
        bot.unload_extension(cog)
    except Exception as error:
        await ctx.send(f'**ERROR:** {error}')
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return
    await ctx.send(f'Successfully unloaded: `{cog}`')

@bot.command()
@commands.is_owner()
async def reload(ctx, *, cog: str):
    try:
        bot.unload_extension(cog)
        bot.load_extension(cog)
    except Exception as error:
        await ctx.send(f'**ERROR:** {error}')
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return
    await ctx.send(f'Successfully reloaded: `{cog}`')

bot.run(config["token"])
