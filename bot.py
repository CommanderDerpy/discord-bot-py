import discord
import customHelp
from discord.ext import commands
from datetime import datetime
# import sys, traceback
import logging
import json
import random

### Logging Config
# TODO: Set up logging
logging.basicConfig(level=logging.INFO)
### Logging Config

### Load Json config
with open('data.json') as f:
		config = json.load(f)
### Load Json config

### Basic Config
version = "0.0.01A"
### Basic Config

help = customHelp.CustomHelp()
bot = commands.Bot(command_prefix='?', description=config['description'], formatter=help)

### Extension Cog Setup
initial_extensions = ['cogs.tarkov']

if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print('Failed to load extension' + sys.stderr)
			traceback.print_exc()
### Extensions Cog Setup

### Overrides
def is_owner():
	async def predicate(ctx):
		return ctx.author.id == config['owner']
	return commands.check(predicate)

@bot.event
async def on_message(message):
	if message.author.id != bot.user.id:
		print(datetime.now().strftime("%I:%M%p on %B %d, %Y")+' - {0.author}: {0.content}'.format(message))
		await bot.process_commands(message)
		pass

@bot.event
async def on_ready():
	print('\nLogged in as: \t\t{bot.user.name}\nUserID:\t\t\t{bot.user.id}\nBot Owner:\t\t' +str(config['owner']) +'\n\nersion: \t\t' +version +'\nDiscord.py Version: \t{discord.__version__}\n')
	print('Successfully logged in and booted...!')

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, discord.ext.commands.CommandOnCooldown):
		await ctx.send(error)
	else:
		randomNumber = str(random.randint(100000,999999))
		await ctx.send("Something went wrong.. but I am not sure what. - Error code #" + randomNumber)
		print("Error code #" +randomNumber + " - " + str(error))


# TODO - Add Custom help method

### Overrides

### Run
# TODO: Set up database
bot.run(config['key'])
### Run