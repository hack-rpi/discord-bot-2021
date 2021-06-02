import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
import on_raw_reaction_add as reaction_add
import base64_encoding as b64

# Useful website: https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

load_dotenv()

global globalReaction
global globalChannelCategory


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("running")

    # !on reaction
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):  # called when a user reacts
        if payload.user_id == bot.user.id:  # Prevent the chat log from being sent to the admin channel before deletion
            return
        channel = bot.get_channel(payload.channel_id)  # get channel id from payload
        message = await channel.fetch_message(payload.message_id)  # get message id from payload
        embed = message.embeds[0]  # get the embed from the message

        if b64.decode(embed.footer.text)[0:9] == "HELP_DESK":  # NOTE TO SELF: CHECK THIS LINE
            await reaction_add.create_help_channel(self, payload, bot)
        elif b64.decode(embed.footer.text) == "DELETE_HELP_CHANNEL":
            await reaction_add.delete_help_channel(self, payload, bot)

    # end of on_raw_reaction_add

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
    async def embed(self, ctx, channelCategory, customTicket, userReaction, *, text):
        await ctx.message.delete()  # immediately deletes original command from chat
        # for customized title, create argument for title, and pass argument into title= 
        embed = discord.Embed(title="HackRPI Help Desk", url="https://hackrpi.com/", description=text, color=0x8E2D25)
        file = discord.File("assets/f20logo.png", filename="f20logo.png")
        embed.set_thumbnail(url="attachment://f20logo.png")
        # set footer
        print(customTicket)
        strng = channelCategory + ";" + customTicket + ";"
        embed.set_footer(text=b64.encode(strng))  # add category to embed footer
        msg = await ctx.send(file=file, embed=embed)

        await msg.add_reaction(userReaction)

        # ! checks for existing category 
        found = False
        for category in ctx.message.guild.categories:
            channelCategory.replace("_", " ")
            if channelCategory == category:
                found = True
                print(found)
                break

        # creates category on embed message send
        # channel name
        name = channelCategory
        # sets category name from command argument
        category = discord.utils.get(ctx.guild.categories, name=name)
        # creates guild
        guild = ctx.message.guild

        if not found:
            # await - execute category creation 
            await ctx.guild.create_category(name)
            print('category created')
        # end of object


# driver
bot = commands.Bot(command_prefix='/', description='Test bot')
bot.add_cog(TestCog(bot))
bot.run(os.getenv("BOT_TOKEN"), bot=True, reconnect=True)
