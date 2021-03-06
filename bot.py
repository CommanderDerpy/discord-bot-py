# Discord.py imports

import discord
import CustomHelp
# Cog Imports
import cogs.tarkov as TarkovCog
import cogs.random as RandomCog
import cogs.admin as AdminCog
# Util imports
import helper.Embed as EmbedHelper
from discord.ext import commands
# Python Imports
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

help = CustomHelp.CustomHelp()
bot = commands.Bot(command_prefix='?', description=config['description'])
# Add Custom help
bot.help_command = CustomHelp.CustomHelp()

# Set up config for bot variable.
bot.config = config
config = None;

### Extension Cog Setup
initial_extensions = [TarkovCog.Tarkov(bot), RandomCog.Random(bot)]

if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.add_cog(extension)
		except Exception as e:
			print('Failed to load extension' + sys.stderr)
			traceback.print_exc()
### Extensions Cog Setup

### Overrides
def is_owner():
	'''
	Overrides Bot Owner.
	'''
	async def predicate(ctx):
		return ctx.author.id == bot.config['owner']
	return commands.check(predicate)

@bot.event
async def on_message(message):
	'''
	This method will timestamp and write every single message recived in the console.
	'''
	if message.author.id != bot.user.id:
		print(datetime.now().strftime("%I:%M%p on %B %d, %Y")+' - {0.author}: {0.content}'.format(message))
		await bot.process_commands(message)
		pass

@bot.event
async def on_ready():
	'''
	Sends a quick message to the console when the bot is ready to be used.
	'''
	print('\nLogged in as: \t\t' + bot.user.name + '\nUserID:\t\t\t' + str(bot.user.id) + '\nBot Owner:\t\t' +str(bot.config['owner']) +'\n\nersion: \t\t' +version +'\nDiscord.py Version: \t' + str(discord.__version__))
	print('Bot has Successfully logged in and is ready to go...!\n\n')

@bot.event
async def on_command_error(ctx, error):
	'''
	If any commands fails this command will notify the user and also give them a error code for easy future debugging.
	'''
	if isinstance(error, discord.ext.commands.CommandOnCooldown):
		await ctx.send(error)
	else:
		randomNumber = "#CMD-" + str(random.randint(100000,999999))
		await ctx.send(embed=EmbedHelper.error("Error processing command", "Something went wrong.. but I am not sure what. - Error code " + randomNumber))
		print("Error code " +randomNumber + " - " + str(error))

### Overrides

### Run
# TODO: Set up database
bot.run(bot.config['key'])
### Run