from twitchio.ext import commands
import logging
import os
from dotenv import load_dotenv
from collections import Counter
import time
import importlib.util
import traceback
from modules.utils import logmessage, NAME, COPYRIGHT, VERSION, BUILDVER, REPO
import json
logging.basicConfig(level=logging.INFO)

with open(os.path.join("data", "log.log"), 'a') as f:
    f.write("\n\n")

logmessage("INFO", f"Startup request received; {NAME} is starting up...", function="STARTUP")
logmessage("INFO", f"{NAME} {VERSION} [Build {BUILDVER}]", function="STARTUP")
logmessage("INFO", f"{COPYRIGHT} - Open sourced @ {REPO}", function="STARTUP")



load_dotenv(dotenv_path=os.path.join("data", "var", "client.env"))
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

BOT_ID = os.getenv('BOT_ID')
CHAT = os.getenv('CHAT')

missing = [var for var in ['OAUTH_TOKEN', 'CLIENT_ID', 'CLIENT_SECRET', 'BOT_ID', 'CHAT'] if not os.getenv(var)]
if missing:
    raise EnvironmentError(f"Missing required environment variables inside data/var/client.env: {', '.join(missing)}")



async def parse_all_modules(bot):
    base_path = os.path.join("structure", "modules")
    logmessage("INFO", f"Parsing modules from {base_path}...", 
               function="parse_all_modules")
    
    results = Counter()
    loadstart = time.perf_counter()

    # If you need to exclude certain folders or files, you can specify them here
    exclude_folders = {
        "disabled",
        "__pycache__",
    }
    exclude_files = {
        "utils.py",
    }

    for root, dirs, files in os.walk(base_path):
        if any(folder in root.split(os.sep) for folder in exclude_folders):
            results["skipped"] += 1
            continue

        for file in files:
            if file.endswith(".py") and file not in exclude_files:
                file_path = os.path.join(root, file)
                try:
                    rel_path = os.path.relpath(file_path, os.path.dirname(base_path))  # Relative path from base_path
                    module_path = rel_path[:-3].replace(os.sep, ".")  # Supported directory structure

                    spec = importlib.util.spec_from_file_location(module_path, file_path)
                    if spec is None:
                        logmessage("ERROR", f"Could not load spec for {module_path}; returned None", 
                                   function="parse_all_modules")
                        results["failed"] += 1
                        continue

                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for attribute in dir(module):
                        attr = getattr(module, attribute)

                        if isinstance(attr, type) and issubclass(attr, commands.Cog) and attr is not commands.Cog:
                            # If a cog is already loaded, remove it before re-adding it, essentially reloading it
                            if attribute in bot.cogs:
                                bot.remove_cog(attribute)

                            cog_instance = attr(bot)
                            bot.add_cog(cog_instance)
                            results["loaded"] += 1
                            logmessage("INFO", f"{module_path} has been loaded successfully!", 
                                       function="parse_all_modules")
                            
                except Exception as e:
                    tb = traceback.format_exc()
                    logmessage("ERROR", f"Failed to load module {module_path}: {e}\n{tb}", 
                               function="parse_all_modules")
                    results["failed"] += 1
                    
            else:
                results["skipped"] += 1

    loadend = time.perf_counter()
    elapsed = round(loadend - loadstart, 1) # Time elasped since loading started
    logmessage("INFO", f"Module parsing completed in {elapsed}s!", function="parse_all_modules")
    logmessage("INFO", f"Successfully loaded {results['loaded']} modules, skipped {results['skipped']} modules, {results['failed']} modules failed to load", function="parse_all_modules")

                        




class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=OAUTH_TOKEN,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            prefix='!',
            initial_channels=[CHAT],
        )

    async def event_ready(self):
        logmessage("INFO", f"Parsing modules...",
                   function="STARTUP")
        await parse_all_modules(self) # Loads modules & reloads if needed

        logmessage("INFO", f"{NAME} is now online under Twitch account {self.nick}!", 
                   function="STARTUP")



    async def event_message(self, message):
        if message.echo:  # Ignore bot's own messages
            return

        logmessage("DEBUG", f"{message.channel.name}.{message.author.name}: {message.content}", 
                member=message.author.name, function="event_message")

        with open(os.path.join("data", "config.json"), "r") as f:
            config = json.load(f)
        ALLOWED_WHEN_DISABLED = config.get("allowed_when_disabled") # configure this in config.json

        ctx = await self.get_context(message)
        togglecontrol = getattr(self, "allowcontrol", True) # If it cant find it, the bot assumes its enabled

        # Only allow commands if control is enabled or it's whitelisted under ALLOWED_WHEN_DISABLED
        if togglecontrol or (ctx.command and ctx.command.name in ALLOWED_WHEN_DISABLED):
            await self.handle_commands(message)



client = Bot()
client.run()