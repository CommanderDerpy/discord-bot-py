# Discord.py imports
import discord
from discord.ext import commands
# Python imports
from datetime import datetime
# Webrequest
import aiohttp
import asyncio
# String re
import re
# Parse html
from bs4 import BeautifulSoup
from discord.ext.commands.cooldowns import BucketType

class Tarkov(commands.Cog):
  TAG_RE = re.compile(r'<[^>]+>')

  def __init__(self, bot):
      self.bot = bot

  @commands.command(name='wiki')
  async def tarkov_search(self, ctx, searchTerm, numberOfResults=1):
      """
        Search the Tarkov wiki for an item

        Parameters:
          Search term - required - This is the search term
          number of posts - optional - default 1 - number of results

        Returns:
            A link to a wiki post related to the search term
      """
      async with ctx.channel.typing():
        # Restrict the number of returned results to 5
        if numberOfResults > 5:
          numberOfResults = 5
          pass
        async with aiohttp.ClientSession() as cs:
          # Replace spaces woth %20?
          searchTerm = searchTerm.replace(" ", "%20")
          async with cs.get('https://escapefromtarkov.gamepedia.com/api.php?action=query&list=search&format=json&srsearch=' + searchTerm) as r:
            res = await r.json()

            embed = discord.Embed(title="Search result", colour=discord.Colour(0x2ecc71))
            embed.set_author(name="Prime", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_footer(text="Tarkov Search", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

            if len(res['query']['search']) > 0:
              counter = 0
              for result in res['query']['search']:
                if counter == numberOfResults:
                    break
                strippedHtmlSnippet = "**Preview: **" +self.TAG_RE.sub('', result['snippet']) + "...\n**Url: https://escapefromtarkov.gamepedia.com/?curid=" +str(result['pageid'])  +"**\n\n"
                embed.add_field(name="**Title:** " +result['title'], value=strippedHtmlSnippet)
                counter+= 1
                pass
            else:
              embed.add_field(name='No result found', value='No Item named ' + searchTerm)
              pass

      await ctx.send(embed=embed)

  @commands.command(name='news')
  @commands.cooldown(1,120,BucketType.default)
  async def tarkov_news(self, ctx):
      """
        Get the latest new from the Offical Tarkov website

        Parameters:
            none

        Returns:
            A link to the latest Tarkov new post.
      """
      url = 'https://www.escapefromtarkov.com'
      async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
          # Replace spaces woth %20?
          async with cs.get('https://www.escapefromtarkov.com/news') as response:
            soup = BeautifulSoup(await response.read(), 'html.parser')
            news_list = soup.find("ul", id="news-list")
            news = news_list.find("li")

            headtext = news.find('div', 'headtext')
            link = headtext.find('a')
            linkHref = link.get('href')
            title = link.get_text()
            snippet = news.find('div', 'description').get_text()

            urlLink = url + linkHref

            embed = discord.Embed(title="Most resent news", colour=discord.Colour(0x2ecc71))
            embed.set_author(name="Prime", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_footer(text="Tarkov News", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            # embed.set_thumbnail(url=image)
            embed.add_field(name="**Title:** " +title, value=snippet + "\n" +urlLink)


            await ctx.send(embed=embed)
            # await ctx.send(title +" - " + urlLink + "\n" +snippet)

  @commands.command(name='newsFive')
  async def tarkov_newsFive(self, ctx):
        """
          This should go :(
        """
        url = 'https://www.escapefromtarkov.com'
        async with ctx.channel.typing():
          async with aiohttp.ClientSession() as cs:
            # Replace spaces woth %20?
            async with cs.get('https://www.escapefromtarkov.com/news') as response:
              embed = discord.Embed(title="Most resent news", colour=discord.Colour(0x2ecc71))
              soup = BeautifulSoup(await response.read(), 'html.parser')
              news_list = soup.find("ul", id="news-list")
              # news = news_list.find("li")
              news = news_list.find_all("li")
              count = 0
              for x in news:
                if count == 5:
                  break
                pass
                headtext = x.find('div', 'headtext')
                link = headtext.find('a')
                linkHref = link.get('href')
                title = link.get_text()
                snippet = x.find('div', 'description').get_text()

                urlLink = url + linkHref

                embed.set_author(name="Prime", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
                embed.set_footer(text="Tarkov News", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
                # embed.set_thumbnail(url=image)
                embed.add_field(name="**Title:** " +title, value=snippet + "\n" +urlLink)
                count+= 1
                pass


              await ctx.send(embed=embed)

  @commands.command(name='links')
  async def tarkov_links(self, ctx):
        """
          A collection of useful links related to Tarkov

          Parameters:
              None

          Returns:
              A collection of useful links
        """
        url = 'https://www.escapefromtarkov.com'
        async with ctx.channel.typing():
          async with aiohttp.ClientSession() as cs:
            embed = discord.Embed(title="Tarkov useful links", colour=discord.Colour(0x2ecc71))
            embed.set_author(name="Prime", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_footer(text="Tarkov Links", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            # embed.set_thumbnail(url=image)
            embed.add_field(name="Useful Tarkov websites with many different resources!", value="[Collection of useful links](http://tarkov.sheiddy.com/Useful)")
            # Quests
            embed.add_field(name="Quests", value="[List of Quests](https://escapefromtarkov.gamepedia.com/Quests)\n[Items to keep](https://d1u5p3l4wpay3k.cloudfront.net/escapefromtarkov_gamepedia/e/e4/QuestItemsToKeep.png?version=1bee34a46818b168ab83fa27976c110e)", inline=True)

            await ctx.send(embed=embed)

  @commands.command(name='maps', description='description on map stuff')
  async def tarkov_maps(self, ctx):
        """
          A collection of maps

          Parameters:
              none

          Returns:
              A collection of maps
        """
        async with ctx.channel.typing():
          async with aiohttp.ClientSession() as cs:
            embed = discord.Embed(title="Tarkov Maps", colour=discord.Colour(0x2ecc71))
            embed.set_author(name="Prime", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_footer(text="Tarkov Maps", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            # Factory
            embed.add_field(name="Factory", value='[Gamepedia](https://escapefromtarkov.gamepedia.com/Factory)\n[Map](https://c-7npsfqifvt34x24e2v6q4m5x78qbz4lx2edmpvegspoux2eofu.g00.gamepedia.com/g00/3_c-7ftdbqfgspnubslpw.hbnfqfejb.dpn_/c-7NPSFQIFVT34x24iuuqtx3ax2fx2fe2v6q4m5x78qbz4l.dmpvegspou.ofux2fftdbqfgspnubslpw_hbnfqfejbx2f3x2f36x2fGbdupszDbmmpvutNbq.kqhx3fwfstjpox3d3ec3b3700d1043679790597ff0d5g744_$/$/$/$/$?i10c.ua=1&i10c.dv=14)\n[Interactive Map](https://eftmkg.com/factory-full.html)', inline=True)
            # Customs
            embed.add_field(name="Customs", value="[Gamepedia](https://escapefromtarkov.gamepedia.com/Customs)\n[Map](https://c-7npsfqifvt34x24e2v6q4m5x78qbz4lx2edmpvegspoux2eofu.g00.gamepedia.com/g00/3_c-7ftdbqfgspnubslpw.hbnfqfejb.dpn_/c-7NPSFQIFVT34x24iuuqtx3ax2fx2fe2v6q4m5x78qbz4l.dmpvegspou.ofux2fftdbqfgspnubslpw_hbnfqfejbx2f7x2f74x2fDvtupnt_4e_Gvmm.kqhx3fwfstjpox3df744b772e31fbf752128e77f5gddf06c_$/$/$/$/$?i10c.ua=1&i10c.dv=14)\n[Interactive Map](https://eftmkg.com/customs-full.html)", inline=True)
            # Woods
            embed.add_field(name="Woods", value="[Gamepedia](https://escapefromtarkov.gamepedia.com/Woods)\n[Map](https://c-7npsfqifvt34x24e2v6q4m5x78qbz4lx2edmpvegspoux2eofu.g00.gamepedia.com/g00/3_c-7ftdbqfgspnubslpw.hbnfqfejb.dpn_/c-7NPSFQIFVT34x24iuuqtx3ax2fx2fe2v6q4m5x78qbz4l.dmpvegspou.ofux2fftdbqfgspnubslpw_hbnfqfejbx2f1x2f17x2fXppetNbqLfzTqbx78otFyjut.kqhx3fwfstjpox3d761bc418d1e19126c2304ff44191544d_$/$/$/$/$?i10c.ua=1&i10c.dv=14)\n[Interactive Map](https://eftmkg.com/woods-full.html)", inline=True)
            # Interchange
            embed.add_field(name="Interchange", value="[Gamepedia](https://escapefromtarkov.gamepedia.com/Interchange)\n[Map](https://c-7npsfqifvt34x24e2v6q4m5x78qbz4lx2edmpvegspoux2eofu.g00.gamepedia.com/g00/3_c-7ftdbqfgspnubslpw.hbnfqfejb.dpn_/c-7NPSFQIFVT34x24iuuqtx3ax2fx2fe2v6q4m5x78qbz4l.dmpvegspou.ofux2fftdbqfgspnubslpw_hbnfqfejbx2f1x2f17x2fJoufsdibohfNbqMpsbuips.kqhx3fwfstjpox3d24ff2bde1109ec31dg3bbed757f21g44_$/$/$/$/$?i10c.ua=1&i10c.dv=14)\n[Interactive Map](https://eftmkg.com/interchange-print.html)", inline=True)
            # Shoreline
            embed.add_field(name="Shoreline", value="[Gamepedia](https://escapefromtarkov.gamepedia.com/Shoreline)\n[Map](https://c-7npsfqifvt34x24e2v6q4m5x78qbz4lx2edmpvegspoux2eofu.g00.gamepedia.com/g00/3_c-7ftdbqfgspnubslpw.hbnfqfejb.dpn_/c-7NPSFQIFVT34x24iuuqtx3ax2fx2fe2v6q4m5x78qbz4l.dmpvegspou.ofux2fftdbqfgspnubslpw_hbnfqfejbx2f6x2f64x2fTipsfmjofNbqTqbx78otFyjutLfzt.kqhx3fwfstjpox3d8c1518bfc09752g40051f1eg668e7ebd_$/$/$/$/$?i10c.ua=1&i10c.dv=14)\n[Sanatorium Map](https://c-7npsfqifvt34x24e2v6q4m5x78qbz4lx2edmpvegspoux2eofu.g00.gamepedia.com/g00/3_c-7ftdbqfgspnubslpw.hbnfqfejb.dpn_/c-7NPSFQIFVT34x24iuuqtx3ax2fx2fe2v6q4m5x78qbz4l.dmpvegspou.ofux2fftdbqfgspnubslpw_hbnfqfejbx2f6x2f66x2fSftpsuSppntOfx78.kqhx3fwfstjpox3d1354gb2806505gebd68ec29c2e61586e_$/$/$/$/$?i10c.ua=1&i10c.dv=14)\n[Interactive Map](https://eftmkg.com/shoreline-full.html)", inline=True)
            # TerraGroup Labs
            embed.add_field(name="TerraGroup Labs", value="[Gamepedia](https://c-4tvylwolbz88x24k8b2w0s1dwhf0rx2ejsvbkmyvuax2eula.g00.gamepedia.com/g00/3_c-4lzjhwlmyvtahyrvc.nhtlwlkph.jvt_/c-4TVYLWOLBZ88x24oaawzx3ax2fx2fk8b2w0s1dwhf0r.jsvbkmyvua.ulax2flzjhwlmyvtahyrvc_nhtlwlkphx2f7x2f7ix2fAolShiThwMbss.wunx3fclyzpvux3dkh7ik881606kj0i9i787h6h46mi359ki_$/$/$/$/$?i10c.ua=1&i10c.dv=21)\n[]()", inline=True)
            # Placeholder
            # embed.add_field(name="Customs", value="[Gamepedia]()\n[Map]()\n[Interactive Map]()", inline=True)

            # TODO - Add more maps
            embed.add_field(name="Other", value="[Interactive Maps (All)](https://eftmkg.com/)", inline=False)
            #  Notes
            embed.add_field(name="Notes", value=" If you would like to add something to this list please message <@100046414670741504>", inline=False)

            await ctx.send(embed=embed)
