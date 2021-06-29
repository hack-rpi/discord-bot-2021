import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
import on_raw_reaction_add as reaction_add
import base64_encoding as b64
import error_checking as err

# Useful website: https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

load_dotenv()

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

        if len(message.embeds) != 0 and message.author.id == bot.user.id:
            embed = message.embeds[0]  # get the embed from the message
            footer = b64.decode(embed.footer.text)

            # Searches footer["type"] for channel type (help / sponsor specific / delete)
            # Check to see the message is from the bot and it is actually an embed message
            if footer["type"] == "HELP_DESK":
                await reaction_add.create_help_channel(self, payload, bot)
            elif footer["type"] == "DELETE_HELP_CHANNEL":
                await reaction_add.delete_help_channel(self, payload, bot)

    #TODO: potentially look into being able to edit the description for the created ticket section
    #TODO: change channel_category to be an ID to an existing category, and update it in create_help_channel when searching
    @commands.command()
    #TODO: use a role by ID from the .env file
    @commands.has_role("admin")
    async def embed(self, ctx, channel_category, custom_ticket, user_reaction, *, text): # asterisk allows for paragraph input
        error_detected, returned_error = err.embed_error_check(channel_category, custom_ticket, user_reaction, text, bot)
        if error_detected:
            if returned_error == "channel string" or returned_error == "ticket string" or returned_error == "text string":
                await ctx.message.delete()  # immediately deletes original command from chat
                return ValueError(f"Invalid input to embed() command for the {returned_error}.")
            elif returned_error == "emoji":
                await ctx.message.delete()  # immediately deletes original command from chat
                return ValueError(f"Invalid emoji entered to the embed() command: \"{user_reaction}\". "
                                  f"Please choose a different emoji.")
        else:
            await ctx.message.delete()  # immediately deletes original command from chat
            # for customized title, create argument for title, and pass argument into title=
            # TODO: support other logos/URLs (probably an uploaded file with the embed command?)
            embed = discord.Embed(title="HackRPI Help Desk", url="https://hackrpi.com/", description=text, color=0x8E2D25)
            file = discord.File("assets/f20logo.png", filename="f20logo.png")
            embed.set_thumbnail(url="attachment://f20logo.png")


            # set footer
            footer = dict()
            footer["category"] = channel_category
            footer["custom_ticket"] = custom_ticket
            footer["ticket_num"] = 0
            footer["type"] = "HELP_DESK"

            #TODO: error checking parameters passed in

            embed.set_footer(text=b64.encode(footer))  # add category to embed footer
            msg = await ctx.send(file=file, embed=embed)

            await msg.add_reaction(user_reaction)

            # ! checks for existing category
            found = False
            for category in ctx.message.guild.categories:
                channel_category.replace("_", " ")
                if channel_category == category:
                    found = True
                    break

            # creates category on embed message send
            # channel name
            name = channel_category
            # sets category name from command argument
            category = discord.utils.get(ctx.guild.categories, name=name)
            # creates guild
            guild = ctx.message.guild

            if not found:
                # await - execute category creation
                await ctx.guild.create_category(name)
            # end of object

    @embed.error
    # TODO: more specific errors with /embed command (assuming an admin ran the command only)
    async def embed_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Invalid usage: /embed ") # Finish this line
        else:
            await ctx.send(str(error))

    @commands.command
    @commands.has_role("admin")
    async def help(self, ctx):
        description = """Embed Creation Command
        /embed <channel category name> <channel header> <reaction emoji> <description in initial embed>
        Note: the first two parameters must be one word, or have zero spaces; the third parameter must
        be a valid emoji; the last parameter can be however long you want it to be"""
        embed = discord.Embed(title="Admin Commands Help", url="https://hackrpi.com/",
            description="A representative will be with you shortly. If your case can be closed, react to this message with the :lock: emoji, and the channel will be deleted.",
            color=0x8E2D25)
        await ctx.send(embed=embed)

# driver
bot = commands.Bot(command_prefix='/', description='Test bot')
bot.add_cog(TestCog(bot))
bot.run(os.getenv("BOT_TOKEN"), bot=True, reconnect=True)
