import discord
from discord.ext import commands
from datetime import datetime

class Random(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='cog_test', hidden=True)
  async def cogTest(self, ctx, *, content='word'):
      """
        The function to add two Complex Numbers.

        Parameters:
            string (str): The complex number to be added.

        Returns:
            ComplexNumber: A complex number which contains the sum.
      """
      await ctx.send('It worked! - ' + content)

  @commands.command()
  async def roll(ctx, dice: str):
      """Rolls a dice in NdN format."""
      try:
          rolls, limit = map(int, dice.split('d'))
      except Exception:
          await ctx.send('Format has to be in NdN!')
          return

      result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
      await ctx.send(result)

  @commands.command(description='For when you wanna settle the score some other way')
  async def choose(ctx, *choices: str):
      """Chooses between multiple choices."""
      await ctx.send(random.choice(choices))

  @commands.command()
  async def repeat(ctx, times: int, content='repeating...'):
      """Repeats a message multiple times."""
      for i in range(times):
          await ctx.send(content)

  @commands.command()
  async def embed(self, ctx):
    """This is an embed test"""
    embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~", colour=discord.Colour(0x92350a), url="https://discordapp.com", description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```", timestamp=datetime.utcfromtimestamp(1545447379))

    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_author(name="author name", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="🤔", value="some of these properties have certain limits...")
    embed.add_field(name="😱", value="try exceeding some of them!")
    embed.add_field(name="🙄", value="an informative error should show up, and this view will remain as-is until all issues are fixed")
    embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
    embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)

    await ctx.send(content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```", embed=embed)

  @commands.command()
  async def joined(ctx, member: discord.Member):
      """Says when a member joined."""
      await ctx.send('{0.name} joined in {0.joined_at}'.format(member))