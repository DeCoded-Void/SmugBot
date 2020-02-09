import discord
from discord.ext import commands
import datetime
import subprocess
import re

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def ping(self, ctx):
        try:
            epoch = datetime.datetime(1970,1,1)
            startnum = (datetime.datetime.utcnow() - epoch).total_seconds()
            msg = await ctx.send('Loading response times, please wait...\n\nIf this message doesn\'t change for a while, uh... :grimacing:')
            lastnum = (datetime.datetime.utcnow() - epoch).total_seconds()
            cmdnum = lastnum - startnum
            cmdnum = round(cmdnum * 1000, 2)

            latency = self.bot.latency * 1000
            latency = str(round(latency, 2))

            command = 'ping discordapp.com -n 1'
            cmd_ping = subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read()
            pattern_recog = r"Average = (\d+)"
            cmd_ping = re.findall(pattern_recog, cmd_ping.decode())[0]
            cmd_ping = format(float(cmd_ping),'.2f')

            embed = discord.Embed(timestamp=datetime.datetime.utcnow())
            embeddesc = str(f':heartbeat: Server Heartbeat: **{latency}ms**\n'
                            f':globe_with_meridians: discordapp.com: **{cmd_ping}ms**\n'
                            f':speech_balloon: Message Speed: **{cmdnum}ms**')
            embed.add_field(name="Latencies:", value=embeddesc, inline=False)
            await msg.edit(content = ':ping_pong: Pong!', embed = embed)
        except Exception as error:
            await ctx.send(f'Unable to ping:\n{error}')

def setup(bot):
    bot.add_cog(ping(bot))
