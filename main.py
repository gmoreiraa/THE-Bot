import os
import discord
from keep_alive import keep_alive
from discord.ext import commands
import asyncio
import music
from text import run

cogs = [music]

client = commands.Bot(command_prefix="-", intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

keep_alive()

bot_token = os.environ['BOT_TOKEN']

loop = asyncio.get_event_loop()
loop.create_task(client.start(bot_token))
run(loop, bot_token)

try:
    loop.run_forever()
finally:
    loop.stop()