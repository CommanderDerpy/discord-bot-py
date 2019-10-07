import discord
import datetime

def setup(title, text):
	embed = discord.Embed(title= ":warning:   " + title + "   :warning:" , description=text + "\n")
	embed.timestamp = datetime.datetime.now()
	return embed
pass

def good(title, text):
	embed = setup(title, text)
	embed.colour = 0x32CD32 
	return embed
pass

def error(title, text):
	embed = setup(title, text)
	embed.colour = 0xff0000 
	return embed
pass
