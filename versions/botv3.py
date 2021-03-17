import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json

client = discord.Client()

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
    async def embed(self, ctx, channelCategory, userReaction, *, text):
        await ctx.message.delete() #immediately deletes original command from chat 
        # for customized title, create argument for title, and pass argument into title= 
        embed=discord.Embed(title="HackRPI Help Desk", url="https://hackrpi.com/", description=text, color=0x8E2D25)
        file = discord.File("assets/f20logo.png", filename="f20logo.png")
        embed.set_thumbnail(url="attachment://f20logo.png") 
        msg = await ctx.send(file=file, embed=embed)
        await msg.add_reaction(userReaction)

        # ! checks for existing category 
        found = False
        for category in ctx.message.guild.categories:
            channelCategory.replace("_", " ")
            if(channelCategory == category):
                found = True
                print(found)
                break

        #creates category on embed message send
        #channel name
        name = channelCategory  
        # sets category name from command argument
        category = discord.utils.get(ctx.guild.categories, name=name)
        # creates guild
        guild = ctx.message.guild

        if(not found):
            # await - execute category creation 
            await ctx.guild.create_category(name)
            print('category created')

        #!on reaction
        while True: #stay running while bot is up
            def check(reaction, user):
                return str(reaction.emoji) == userReaction and user != bot.user

            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            
            print("Channel created for {}".format(user.name))   #await ctx.send

            #search for current ticket count
            with open("assets/ticketCount.json", "r") as f:
                data = json.load(f) 
            ticketNumber = int(data['ticket-counter']) 

            #increase count
            ticketNumber += 1

            #!imp privacy overwrites 
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                user: discord.PermissionOverwrite(read_messages=True) #!imp adds user permissions 
            }

            # create private ticket text channel 
            name = channelCategory  
            # sets category name from command argument
            category = discord.utils.get(ctx.guild.categories, name=name)
            categoryFin = category #stops channels from going public

            #!creates channel inside of category
            #set counter to 0, to make sure only 1 ticket is created 
            await ctx.guild.create_text_channel("Ticket-{:04d}".format(ticketNumber), category=categoryFin, overwrites=overwrites) 
            #channel = discord.utils.get(guild.text_channels, name = "Ticket-{:04d}".format(ticketNumber))
            
            #update json file with ticket count 
            data["ticket-counter"] = ticketNumber
            with open("assets/ticketCount.json", "w") as write_file:
                json.dump(data, write_file)

#run
bot = commands.Bot(command_prefix='/', description='Test bot')
bot.add_cog(TestCog(bot))
bot.run(os.getenv("BOT_TOKEN"), bot=True, reconnect=True)