from twitchio.ext import commands
from modules.utils import logmessage


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def help(self, ctx, category: str = None):
        if category not in ("mouse", "keyboard", "mod"):
            await ctx.send(f"{ctx.author.mention}, invalid category provided. Usage: '!help <mouse/keyboard/mod>'")
            logmessage("DEBUG", f"{ctx.author.name} used invalid arguments for !help",
                    member=ctx.author.name, function="help")
            return
        
        # For this design we have to manually make !help; It looks nice though!
        if category == "mouse":
            await ctx.send(
                f"🖱️ Mouse Commands {ctx.author.mention} | "
                "!click <left/right> | "
                "!goto <x> <y> | "
                "!pos | "
                "!center | "
                "!drag <x> <y> | "
                "!scroll <up/down> <amount> | "
                "!tiny/small/big[direction, 'up,down,left,right']"
            )

        elif category == "keyboard":
            await ctx.send(
                f"⌨️ Keyboard Commands {ctx.author.mention} | "
                "!type <content> | "
                "!keybind <keybind, ex. 'ctrl+shift+esc'> | "
                "!holdkey <key> <duration> | "
                "!clear: Clears selected text"
            )
            
        elif category == "mod":
            await ctx.send(
                f"🛠️ Moderator Commands {ctx.author.mention} | "
                "!togglecontrol: Toggle global control for the host"
            )



def prepare(bot):
    bot.add_cog(HelpCommand(bot))
