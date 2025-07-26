from twitchio.ext import commands
from modules.utils import logmessage

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.event()
    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return # prevents spam

        elif isinstance(error, commands.MissingRequiredArgument):
            # if you want to add stuff here for missing required arguments, do it here!
            return

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"{ctx.author.mention}, that command is on cooldown. Try again in {error.retry_after:.1f} seconds.")
            logmessage("INFO", f"{ctx.author.name} is under cooldown; {error.retry_after:1f}s remaining on cooldown",
                       member=ctx.author.name, function="event_command_error")

        else:
            await ctx.send(f"{ctx.author.mention}, an unexpected error occurred.")
            logmessage("ERROR", f"Unhandled error from {ctx.author.name}: {repr(error)}",
                       member=ctx.author.name, function="event_command_error")

def prepare(bot):
    bot.add_cog(ErrorHandler(bot))
