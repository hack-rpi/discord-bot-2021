import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("running")

    # REGULAR CHANNEL MESSAGE
    @commands.command()
    #  takes arguments self = /create, ctx = default channel (no user input)
    #  channelCategory = channel category, reaction = emoji reaction, 
    #  text = user's paragraph text
    async def create(self, ctx, channelCategory, reaction, *, text): 
        msg = await ctx.send(text)
        # .add_reaction adds reaction to msg
        # test case -> emoji = '👍' 
        await msg.add_reaction(reaction)
        print("success:  emoji added")

    # EMBED MESSAGE
    @commands.command()
    async def embed(self, ctx, channelCategory, reaction, *, text):
         # for customized title, create argument for title, and pass argument into title= 
        embed=discord.Embed(title="HackRPI", url="https://hackrpi.com/", description=text, color=0xFF5733)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(reaction)
        print("embed success")
       
bot = commands.Bot(command_prefix='/', description='Test bot')
bot.add_cog(TestCog(bot))
bot.run(os.getenv("BOT_TOKEN"), bot=True, reconnect=True)