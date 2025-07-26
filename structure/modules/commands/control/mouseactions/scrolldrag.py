from twitchio.ext import commands
from modules.utils import logmessage
import pyautogui


class ScrollDrag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="drag")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def drag_command(self, ctx, x: str = None, y: str = None):
        if x is None or y is None:
            await ctx.send(f"{ctx.author.mention}, Invalid arguments! Usage: '!drag <end-x> <end-y>'")
            return

        try:
            x_val = int(x)
            y_val = int(y)

        except ValueError:
            await ctx.send(f"{ctx.author.mention}, Please provide integer coordinates!")
            return

        screen_width, screen_height = pyautogui.size()
        end_x = max(0, min(screen_width - 1, x_val))
        end_y = max(0, min(screen_height - 1, y_val))

        pyautogui.dragTo(end_x, end_y, duration=0.5)
        logmessage("DEBUG", f"Dragged from current pos to ({end_x}, {end_y}) by {ctx.author.name}", 
                member=ctx.author.name, function="drag")
    

    @commands.command(name="scroll")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def scroll_command(self, ctx, direction: str = None, amount: int = 200):
        direction = (direction or "").lower()

        if direction not in ("up", "down"):
            await ctx.send(f"{ctx.author.mention}, Invalid direction! Use `!scroll up [amount in px]` or `!scroll down [amount in px]`")
            logmessage("DEBUG", f"Invalid scroll direction by {ctx.author.name}", 
                       member=ctx.author.name, function="scroll")
            return

        scroll_amount = amount if direction == "up" else -amount
        pyautogui.scroll(scroll_amount)

        logmessage("DEBUG", f"Scrolled {direction} by {abs(scroll_amount)} from {ctx.author.name}", 
                   member=ctx.author.name, function="scroll")




def prepare(bot):
    bot.add_cog(ScrollDrag(bot))
