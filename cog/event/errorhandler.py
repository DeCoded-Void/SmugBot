import discord
from discord.ext import commands
import sys
import traceback

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Prevents local errors being used with this global one
        if hasattr(ctx.command, 'on_error'):
            return

        # When global cooldown is being used
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            seconds = round(seconds, 2)
            await ctx.send(f'{ctx.author.mention}, {ctx.prefix}{ctx.command} is in cooldown for another {seconds}s :timer:')
            return

        # If command does not exist
        if isinstance(error, commands.CommandNotFound):
            return

        # When the user doesn't give proper arguments
        if isinstance(error, commands.UserInputError):
            await ctx.send(f'Bad arguments or you did not use the command properly...\n\nUse: `{ctx.prefix}help {ctx.command}`\nTo check the formatting.')
            return

        # General CheckFalure error
        if isinstance(error, commands.CheckFailure):

            # If user is not Owner
            if isinstance(error, commands.NotOwner):
                return

            # For Server only commands
            if isinstance(error, commands.NoPrivateMessage):
                await ctx.send(f'> `{ctx.prefix}{ctx.command}`\ncannot be used in DMs.')
                return

            # When the user is missing permission
            if isinstance(error, commands.MissingPermissions):
                if ctx.guild is None:
                    await ctx.send(f'> `{ctx.prefix}{ctx.command}`\ncannot be used in DMs.')
                    return
                await ctx.send(f'You need to have the `{"`, `".join(error.missing_perms)}` permission to use this command.')
                return

            # When the bot is missing permission
            if isinstance(error, commands.BotMissingPermissions):
                if ctx.guild is None:
                    await ctx.send(f'An error is detected, the command used may not work as intended in DMs')
                    return
                await ctx.send(f'I need to have the `{"`, `".join(error.missing_perms)}` permission to use this command.')
                return

            # When the user is missing permission
            if isinstance(error, commands.MissingRole):
                if ctx.guild is None:
                    await ctx.send(f'An error is detected, the command used may not work as intended in DMs')
                    return
                await ctx.send(f'You need to have the `{"`, `".join(error.missing_role)}` role to use this command.')
                return

            # When the bot is missing permission
            if isinstance(error, commands.BotMissingRole):
                if ctx.guild is None:
                    await ctx.send(f'An error is detected, the command used may not work as intended in DMs')
                    return
                await ctx.send(f'I need to have the `{"`, `".join(error.missing_role)}` role to use this command.')
                return

            # When the user is missing permission
            if isinstance(error, commands.MissingAnyRole):
                if ctx.guild is None:
                    await ctx.send(f'An error is detected, the command used may not work as intended in DMs')
                    return
                await ctx.send(f'You need to have one of the roles: `{"`, `".join(error.missing_role)}` to use this command.')
                return

            # default error
            errortxt = 'You or the bot don\'t have the proper permission to run this command.'
            errortxt = errortxt+f'\nUse: `{ctx.prefix}help {ctx.command}`\nTo check the permissions.'
            if ctx.guild is None:
                await ctx.send(errortxt+'\n\nIt\'s also possible that this command cannot be used in DMs.')
                return
            await ctx.send(errortxt)
            return

        # Default Traceback/error
        await ctx.send(':pensive:')
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
