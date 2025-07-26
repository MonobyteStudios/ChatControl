from twitchio.ext import commands
from modules.utils import AHK_PATH, logmessage
import os, platform, asyncio
import json

keybind_map = { # Insert definitions for every value (Ctrl = ^, esc = {Esc})
    "ctrl": "^",
    "control": "^",
    "alt": "!",
    "shift": "+",
    "win": "#",
    "delete": "{Del}",
    "del": "{Del}",
    "tab": "{Tab}",
    "esc": "{Esc}",
    "escape": "{Esc}",
    "enter": "{Enter}",
    "space": "{Space}",
    "f4": "{F4}",
    "f11": "{F11}"
}

def convert_to_ahk_keys(user_input: str) -> str:
    parts = user_input.lower().split("+")
    ahk_keys = ""
    for part in parts:
        ahk_keys += keybind_map.get(part, part)
    return ahk_keys


class KeyboardActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.busy = False

    @commands.command(name="type")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def typemessage(self, ctx, *, text: str = None):
        if not text:
            await ctx.send(f"{ctx.author.mention}, invalid arguments provided! Usage: '!type <text>'.")
            return

        if platform.system() != "Windows":
            await ctx.send("!type unavailable: Host operating system is not using Windows.")
            logmessage("DEBUG", f"!type unavailable: Host operating system is not using Windows.",
                       member=ctx.author.name, function="type")
            return

        if "+" in text:
            await ctx.send(f"{ctx.author.mention}, you can't include keybinds in !type. Please use !keybind instead!")
            return

        if self.busy:
            await ctx.send(f"{ctx.author.mention}, another keyboard operation is currently running. Please wait!")
            return
        
        script_path = os.path.abspath(os.path.join("AutoHotKey", "scripts", "keybinds.ahk"))
        self.busy = True
        try:
            proc = await asyncio.create_subprocess_exec(
                AHK_PATH, script_path, text,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            logmessage("DEBUG", f"{ctx.author.name} used !type: {text}",
                       member=ctx.author.name, function="type")
            
            await proc.wait() # create_subprocess_exec doesn't wait; so we wait for it here

        finally:
            self.busy = False



    @commands.command(name="keybind")
    @commands.cooldown(rate=1, per=3, bucket=commands.Bucket.user)
    async def keybindcommand(self, ctx, *, keys: str = None):
        if not keys:
            await ctx.send(f"{ctx.author.mention}, invalid arguments! Usage: '!keybind <keys>'.")
            raise RuntimeError("This command can only be used on Windows.")

        if platform.system() != "Windows":
            await ctx.send("!keybind unavailable: Host operating system is not using Windows.")
            logmessage("DEBUG", f"!keybind unavailable; Host operating system is not using Windows.",
                    member=ctx.author.name, function="keybind")
            return

        if self.busy:
            await ctx.send(f"{ctx.author.mention}, another keyboard operation is currently running. Please wait!")
            return


        with open(os.path.join("data", "config.json"), "r") as f:
            config = json.load(f)
        disallowed = config.get("blacklisted_keybinds") # configure this in config.json


        lower = keys.lower().replace(" ", "")
        if lower in disallowed:
            await ctx.send(f"{ctx.author.mention}, that key combination is disallowed.")
            logmessage("NOTICE", f"{ctx.author.name} attempted to use a disallowed keybind: {lower}",
                    member=ctx.author.name, function="keybind")
            return


        def is_valid_keybind(user_input: str) -> bool:
            parts = user_input.lower().replace(" ", "").split("+")
            if not parts:
                return False

            non_keybinds = 0
            for part in parts:
                if part not in keybind_map:
                    if len(part) > 1: # Only allow one character in there [Allows keybinds like win+r]
                        return False
                    
                    else:
                        non_keybinds += 1 # If there is more than 1 non_keybind's, return False
                        if non_keybinds > 1:
                            return False

            return True



        if not is_valid_keybind(keys):
            await ctx.send(f"{ctx.author.mention}, only pure keybinds are allowed! [Ex. ctrl+shift+esc]")
            logmessage("DEBUG", f"Invalid request for !keybind: {keys}",
                       member=ctx.author.name, function="keybind")
            return
        

        script_path = os.path.abspath(os.path.join("AutoHotKey", "scripts", "keybinds.ahk"))
        self.busy = True
        try:
            ahk_keys = convert_to_ahk_keys(keys)
            proc = await asyncio.create_subprocess_exec(
                AHK_PATH, script_path, ahk_keys,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            logmessage("DEBUG", f"{ctx.author.name} triggered keybind: {keys} -> {ahk_keys}",
                       member=ctx.author.name, function="keybind")
            
            await proc.wait() # Waits untill process exits

        finally:
            self.busy = False

def prepare(bot):
    bot.add_cog(KeyboardActions(bot))
