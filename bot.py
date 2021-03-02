import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        pass

bot = commands.Bot(command_prefix='/', description='Test bot')
bot.run(os.getenv("BOT_TOKEN"), bot=True, reconnect=True)