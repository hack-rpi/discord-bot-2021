import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json

load_dotenv()

global globalReaction 
global globalChannelCategory  
class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("running")

    #!on reaction
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload): #called when a user reacts
        user = await self.bot.fetch_user(payload.user_id) 
        if user != bot.user:
            channel = bot.get_channel(payload.channel_id)  # get channel id from payload
            message = await channel.fetch_message(payload.message_id)  # get message id from payload
            embed = message.embeds[0].to_dict()

            # if embed.footer == "HELP_DESK": # NOTE TO SELF: CHECK THIS LINE
            print("Channel created for {}".format(user.name))   #await ctx.send
            #search for current ticket count
            with open("../assets/ticketCount.json", "r") as f:
                data = json.load(f)
            ticketNumber = int(data['ticket-counter'])

            #increase count
            ticketNumber += 1

            guild = self.bot.get_guild(payload.guild_id)

            #!imp privacy overwrites
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True), #admin user permissions (add admin role and set permissions for more helpers)
                user: discord.PermissionOverwrite(read_messages=True) #!imp adds user permissions
            }

            # create private ticket text channel  #!imp - hard coded category name
            name = "HELP_DESK"
            # sets category name from command argument
            guild = bot.get_guild(payload.guild_id)

            category = discord.utils.get(guild.categories, name=name)
            categoryFin = category #stops channels from going public
            #!creates channel inside of category
            await guild.create_text_channel("Ticket-{:04d}".format(ticketNumber), category=categoryFin, overwrites=overwrites)

            #remove emoji after channel creation:
            channel = bot.get_channel(payload.channel_id) #get channel id from payload
            message = await channel.fetch_message(payload.message_id) #get message id from payload
            await message.remove_reaction(payload.emoji.name, user) #remove user's emoji reaction

            #update json file with ticket count
            data["ticket-counter"] = ticketNumber
            with open("../assets/ticketCount.json", "w") as write_file:
                json.dump(data, write_file)

            #!CURRENT
            '''get info from embed footer
               if (footer text = delete_help_channel): delete user channel on reaction
               if (footer text = help_channel): create user channel (above) on reaction'''
            #!create new embed in user's channel
            # for customized title, create argument for title, and pass argument into title=
            embed=discord.Embed(title="We are happy to assist you!", url="https://hackrpi.com/", description="A representative will be with you shortly. If your case can be closed, react to this message with the :lock: emoji, and the channel will be deleted.", color=0x8E2D25)
            file = discord.File("assets/f20logo.png", filename="f20logo.png")
            embed.set_thumbnail(url="attachment://f20logo.png")
            #set footer
            embed.set_footer(text="delete_help_channel") #add category to embed footer
            channel = discord.utils.get(guild.channels, name="Ticket-{:04d}".format(ticketNumber))
            channel_id = channel.id
            channel = bot.get_channel(channel_id)
            msg = await channel.send(file=file, embed=embed)

            await msg.add_reaction(":lock:")
            # elif embed.footer == "DELETE":
            #     channel.delete()

    #end of on_raw_reaction_add

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
        #set footer
        embed.set_footer(text=channelCategory) #add category to embed footer 
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
# end of object

# driver
bot = commands.Bot(command_prefix='/', description='Test bot')
bot.add_cog(TestCog(bot))
bot.run(os.getenv("BOT_TOKEN"), bot=True, reconnect=True)