from twitchio.ext import commands
from modules.utils import logmessage, AHK_PATH
import subprocess
import os
import platform
import asyncio

class HoldKey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.busy = False

    @commands.command(name="holdkey")
    @commands.cooldown(rate=1, per=5, bucket=commands.Bucket.user)
    async def holdkey(self, ctx, key: str = None, duration: str = None):
        if platform.system() != "Windows":
            await ctx.send("Command !holdkey unavailable; Host operating system is not using Windows.")
            raise RuntimeError("This command can only be used on Windows.")

        if self.busy:
            await ctx.send(f"{ctx.author.mention}, another keyboard operation is currently running. Please wait!")
            return

        if not key or not duration:
            await ctx.send(f"{ctx.author.mention}, Invalid arguments; Usage: '!holdkey <key> <duration>'")
            return

        key = key.lower()
        if len(key) != 1:
            await ctx.send(f"{ctx.author.mention}, key must be exactly 1 character.")
            return

        try:
            converted_duration = float(duration)
            
        except ValueError:
            await ctx.send(f"{ctx.author.mention}, duration must be a valid number.")
            return

        if converted_duration <= 0 or converted_duration > 20:
            await ctx.send(f"{ctx.author.mention}, duration must be between 1 and 20 seconds.")
            return

        self.busy = True
        script_path = os.path.abspath(os.path.join("AutoHotKey", "scripts", "holdkey.ahk"))
        try:
            proc = await asyncio.create_subprocess_exec(
                AHK_PATH, script_path, key, str(converted_duration),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            logmessage("DEBUG", f"Holding key '{key}' for {converted_duration}s by {ctx.author.name}",
                       member=ctx.author.name, function="holdkey")
            
            await proc.wait() # Normally create_subprocess_exec won't wait until its finished, so we wait for it here

        finally:
            self.busy = False



    @commands.command(name="clear")
    async def clear_command(self, ctx):
        if platform.system() != "Windows":
            await ctx.send("Command !clear unavailable; Host operating system is not running Windows.")
            raise RuntimeError("This command can only be used on Windows.")

        ahk_keys = "^a{Backspace}"  # ^ is Ctrl
        script_path = os.path.abspath(os.path.join("AutoHotKey", "scripts", "keybinds.ahk"))
        
        subprocess.Popen([AHK_PATH, script_path, ahk_keys])
        logmessage("DEBUG", f"{ctx.author.name} used !clear",
                   member=ctx.author.name, function="clear")


def prepare(bot):
    bot.add_cog(HoldKey(bot))
