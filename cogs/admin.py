import discord
from discord.ext import commands
from datetime import datetime

def setup(bot):
	COG_NAME = 'Admin'
	COG_NUM_FUNCTIONS = '0';
	bot.add_cog(Admin(bot))
	print('Loading Cog - ' +COG_NAME +' - ' +COG_NUM_FUNCTIONS + ' functions')

class Admin:

	def __init__(self, bot):
		self.bot = bot

	def checkRoleAbleToAssign(self, strRole):
		for role in self.bot.config['assignable_roles']:
			if strRole.casefold() == role.casefold():
				return True
				pass
			pass
		pass

	def getRole(self, ctx, role):
		for guildRole in ctx.guild.roles:
			if guildRole.name.casefold() == role:
				return guildRole
				pass
			pass
		pass

	@commands.command(name='iam', case_insensitive=True)
	async def iam(self, ctx, roleToAssign=None):
		"""
			X

			Parameters:
					x

			Returns:
					x
		"""
		if not roleToAssign:
			await ctx.send('You can assign the following roles: ' + str(self.bot.config['assignable_roles']))
			pass
		else:
			# Check if role is eligible to be added
			roleEligible = self.checkRoleAbleToAssign(roleToAssign)
			if not roleEligible:
				await ctx.send('This role is not eligible for self assign')
				pass
			else:
				# Get the role from discord
				targetRole = self.getRole(ctx, roleToAssign)
				# Go through all the roles and check if the desired role already exists
				role_iterator = iter(ctx.author.roles)
				next(role_iterator)
				roleExists = False
				for role in role_iterator:
					if role == targetRole:
						roleExists = True
						pass
					pass

				# Add or remove role depending on outcome
				toSend = None;
				if roleExists:
					await ctx.author.remove_roles(targetRole, reason='User REMOVED role with iam command')
					toSend = 'Done - I have removed the role ' +targetRole.name + ' to you'
					pass
				else:
					await ctx.author.add_roles(targetRole, reason='User ADDED role with iam command')
					toSend = 'Done - I have added the role ' +targetRole.name + ' to you'
					pass
				await ctx.send(toSend)