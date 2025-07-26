from twitchio.ext import commands
from modules.utils import logmessage
import pyautogui


class ClickActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="click")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def click(self, ctx, button: str = "left"):
        button = button.lower()
        logmessage("DEBUG", f"Command invoked: !click {button} by {ctx.author.name}", 
                   member=ctx.author.name, function="click")

        if button == "left":
            pyautogui.click()
        elif button == "right":
            pyautogui.rightClick()

        else:
            await ctx.send(f"{ctx.author.mention}, invalid button to press. Usage: '!click <left/right>'")
            return


    @commands.command(name="center")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def center_command(self, ctx):
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        pyautogui.moveTo(center_x, center_y)
        logmessage("DEBUG", f"Moved to center ({center_x}, {center_y}) by {ctx.author.name}",
                member=ctx.author.name, function="center")
        

    @commands.command(name="pos")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def pos_command(self, ctx):
        x, y = pyautogui.position()
        await ctx.send(f"{ctx.author.mention}, Current mouse position: ({x}, {y})")
        logmessage("DEBUG", f"Reported mouse position to {ctx.author.name}: ({x}, {y})",
                member=ctx.author.name, function="pos")



    @commands.command(name="goto")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def goto_command(self, ctx, x: int = None, y: int = None):
        if x is None or y is None:
            await ctx.send(f"{ctx.author.mention}, Invalid arguments! Usage: '!goto <x> <y>'")
            logmessage("DEBUG", f"Invalid arguments for !goto command by {ctx.author.name}", 
                    member=ctx.author.name, function="goto")
            return

        # Prevent x,y coordinates from going off screen
        screen_width, screen_height = pyautogui.size()
        new_x = max(0, min(screen_width - 1, x))
        new_y = max(0, min(screen_height - 1, y))

        pyautogui.moveTo(new_x, new_y)
        logmessage("DEBUG", f"Command successfully parsed, moved mouse to ({new_x}, {new_y})!", 
                member=ctx.author.name, function="goto")
        



def prepare(bot):
    bot.add_cog(ClickActions(bot))
