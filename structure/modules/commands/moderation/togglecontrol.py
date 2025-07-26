from twitchio.ext import commands
from modules.utils import logmessage

class ToggleControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.allowcontrol = True # A global value that handles control commands

    @commands.command(name="togglecontrol")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def togglecontrol(self, ctx):
        if ctx.author.is_mod:
            ctx.bot.allowcontrol = not ctx.bot.allowcontrol

            await ctx.send(f"{ctx.author.mention}, Chat control is now {'enabled ✅' if ctx.bot.allowcontrol else 'disabled ❌'}")
            logmessage("DEBUG", f"{ctx.author.name} used !togglecontrol; New status: {ctx.bot.allowcontrol}",
                    member=ctx.author.name, function="togglecontrol")

        else:
            await ctx.send(f"{ctx.author.mention}, this command is available for channel moderators!")
            logmessage("DEBUG", f"{ctx.author.name} attempted to run !togglecontrol without moderator permissions",
                    member=ctx.author.name, function="togglecontrol")



def prepare(bot):
    bot.add_cog(ToggleControl(bot))
