from twitchio.ext import commands
from modules.utils import logmessage
import pyautogui


class IncrementMovementCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.register_movement_commands()


    def register_movement_commands(self): # Registers the tiny[direction], small[direction], and big[direction] commands
        def scale_by_resolution(percent_x, percent_y):
            screen_width, screen_height = pyautogui.size()
            return int(screen_width * percent_x), int(screen_height * percent_y)

        movement_map = { # Uses percentage of the screen to calculate how far the mouse goes [fits screen resolutions]
            "tinyleft": scale_by_resolution(-0.01, 0),
            "tinyright": scale_by_resolution(0.01, 0),
            "tinyup": scale_by_resolution(0, -0.01),
            "tinydown": scale_by_resolution(0, 0.01),

            "smallleft": scale_by_resolution(-0.03, 0),
            "smallright": scale_by_resolution(0.03, 0),
            "smallup": scale_by_resolution(0, -0.03),
            "smalldown": scale_by_resolution(0, 0.03),

            "bigleft": scale_by_resolution(-0.15, 0),
            "bigright": scale_by_resolution(0.15, 0),
            "bigup": scale_by_resolution(0, -0.15),
            "bigdown": scale_by_resolution(0, 0.15),
        }

        screen_width, screen_height = pyautogui.size()

        for name, (dx, dy) in movement_map.items():
            async def move(self, ctx, dx=dx, dy=dy, name=name):
                x, y = pyautogui.position()
                new_x = max(0, min(screen_width - 1, x + dx))
                new_y = max(0, min(screen_height - 1, y + dy))

                pyautogui.moveTo(new_x, new_y)
                logmessage("DEBUG", f"{name} movement: from ({x}, {y}) to ({new_x}, {new_y}) by {ctx.author.name}",
                        member=ctx.author.name, function=name)

            move.__name__ = f"{name}_command"
            cmd = commands.command(name=name)(move)
            cmd = commands.cooldown(rate=1, per=1, bucket=commands.Bucket.user)(cmd)
            setattr(self, move.__name__, cmd)




def prepare(bot):
    bot.add_cog(IncrementMovementCmds(bot))
