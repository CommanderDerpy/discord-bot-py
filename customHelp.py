import itertools
import inspect
from discord.ext import commands
from discord.ext.commands import GroupMixin, Command

class Paginator:
	"""A class that aids in paginating code blocks for Discord messages.
	Attributes
	-----------
	prefix: :class:`str`
			The prefix inserted to every page. e.g. three backticks.
	suffix: :class:`str`
			The suffix appended at the end of every page. e.g. three backticks.
	max_size: :class:`int`
			The maximum amount of codepoints allowed in a page.
	"""
	def __init__(self, prefix='```', suffix='```', max_size=2000):
			self.prefix = prefix
			self.suffix = suffix
			self.max_size = max_size - len(suffix)
			self._current_page = [prefix]
			self._count = len(prefix) + 1 # prefix + newline
			self._pages = []

	def add_line(self, line='', *, empty=False):
			"""Adds a line to the current page.
			If the line exceeds the :attr:`max_size` then an exception
			is raised.
			Parameters
			-----------
			line: str
					The line to add.
			empty: bool
					Indicates if another empty line should be added.
			Raises
			------
			RuntimeError
					The line was too big for the current :attr:`max_size`.
			"""
			if len(line) > self.max_size - len(self.prefix) - 2:
					raise RuntimeError('Line exceeds maximum page size %s' % (self.max_size - len(self.prefix) - 2))

			if self._count + len(line) + 1 > self.max_size:
					self.close_page()

			self._count += len(line) + 1
			self._current_page.append(line)

			if empty:
					self._current_page.append('')
					self._count += 1

	def close_page(self):
			"""Prematurely terminate a page."""
			self._current_page.append(self.suffix)
			self._pages.append('\n'.join(self._current_page))
			self._current_page = [self.prefix]
			self._count = len(self.prefix) + 1 # prefix + newline

	@property
	def pages(self):
			"""Returns the rendered list of pages."""
			# we have more than just the prefix in our current page
			if len(self._current_page) > 1:
					self.close_page()
			return self._pages

	def __repr__(self):
			fmt = '<Paginator prefix: {0.prefix} suffix: {0.suffix} max_size: {0.max_size} count: {0._count}>'
			return fmt.format(self)

class CustomHelp(commands.HelpFormatter):

	def get_ending_note(self):
		command_name = self.context.invoked_with
		return "Type {0}{1} command for more info on a command.\n" \
			"You can also type \"{0}{1} <category>\" for more info on a category and \"{0}{1} <command>\" for more info on a specific command".format(self.clean_prefix, command_name)

	async def format(self):
		"""Handles the actual behaviour involved with formatting.
		To change the behaviour, this method should be overridden.
		Returns
		--------
		list
				A paginated output of the help command.
		"""
		self._paginator = Paginator()

		# we need a padding of ~80 or so

		description = self.command.description if not self.is_cog() else inspect.getdoc(self.command)

		if description:
				# <description> portion
				self._paginator.add_line(description, empty=True)

		if isinstance(self.command, Command):
				# <signature portion>
				signature = self.get_command_signature()
				self._paginator.add_line(signature, empty=True)

				# <long doc> section
				if self.command.help:
						self._paginator.add_line(self.command.help, empty=True)

				# end it here if it's just a regular command
				if not self.has_subcommands():
						self._paginator.close_page()
						return self._paginator.pages

		max_width = self.max_name_size

		def category(tup):
				cog = tup[1].cog_name
				# we insert the zero width space there to give it approximate
				# last place sorting position.
				return "\n"+ cog + ':' if cog is not None else '\n\u200bNo Category:'

		filtered = await self.filter_command_list()
		if self.is_bot():
				data = sorted(filtered, key=category)
				for category, commands in itertools.groupby(data, key=category):
						# there simply is no prettier way of doing this.
						commands = sorted(commands)
						if len(commands) > 0:
								self._paginator.add_line(category)

						self._add_subcommands_to_page(max_width, commands)
		else:
				filtered = sorted(filtered)
				if filtered:
						self._paginator.add_line('Commands:')
						self._add_subcommands_to_page(max_width, filtered)

		# add the ending note
		self._paginator.add_line()
		ending_note = self.get_ending_note()
		self._paginator.add_line(ending_note)
		return self._paginator.pages