import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
import on_raw_reaction_add as reaction_add
import base64_encoding as b64
import error_checking as err
from discord.utils import get

# Useful website: https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

load_dotenv()

# enable on_member_join functionality
intents = discord.Intents.default()
intents.members = True

class TestCog(commands.Cog):
    
    #! SERVER VARIABLES HARD CODED FOR DEV. EDIT FOR PROD
    # Servers
    MAIN_SERVER = int(os.getenv("MAIN_SERVER"))
    EXPO_SERVER = int(os.getenv("EXPO_SERVER"))
 
    #Add additional sponsor / HackRPI roles for expo server  
    EXPO_ATTENDEE_ROLE = int(os.getenv("EXPO_ATTENDEE_ROLE"))
    EXPO_JUDGE_ROLE = int(os.getenv("EXPO_JUDGE_ROLE"))

    # Main server roles to be retrieved
    MAIN_ATTENDEE_ROLE = int(os.getenv("MAIN_ATTENDEE_ROLE"))
    MAIN_JUDGE_ROLE = int(os.getenv("MAIN_JUDGE_ROLE"))
    
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

    # TODO: potentially look into being able to edit the description for the created ticket section
    # TODO: change channel_category to be an ID to an existing category, and update it in create_help_channel when searching
    @commands.command()
    @commands.has_role(int(os.getenv("MAIN_ADMIN_ROLE")))
    async def embed(self, ctx, channel_category, custom_ticket, user_reaction, *,
                    text):  # asterisk allows for paragraph input
        err.embed_error_check(channel_category, custom_ticket, user_reaction, text, bot)

        await ctx.message.delete()  # immediately deletes original command from chat
        # for customized title, create argument for title, and pass argument into title=
        # TODO: support other logos/URLs (probably an uploaded file with the embed command?)
        embed = discord.Embed(
            title="HackRPI Help Desk",
            url="https://hackrpi.com/",
            description=text,
            color=0x8E2D25,
        )
        file = discord.File("assets/f20logo.png", filename="f20logo.png")
        embed.set_thumbnail(url="attachment://f20logo.png")

        # set footer
        footer = dict()
        footer["category"] = channel_category
        footer["custom_ticket"] = custom_ticket
        footer["ticket_num"] = 0
        footer["type"] = "HELP_DESK"

        # TODO: error checking parameters passed in - Jacob

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
    # TODO: more specific errors with /embed command (assuming an admin ran the command only) - Jacob - COMPLETED
    async def embed_error(self, ctx, error):
        in_message = ctx.message.content
        out_message = f"Invalid usage: '{in_message}'.\n\t"
        if isinstance(error, commands.errors.MissingRequiredArgument):
            # Exception raised when parsing a command and a parameter that is required is not encountered.
            # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.UserInputError
            await ctx.send(out_message + "This embed is missing a required argument.")
        elif isinstance(error, commands.errors.ArgumentParsingError):
            # An exception raised when the parser fails to parse a user’s input.
            # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.UserInputError
            await ctx.send(
                out_message + "The parser was unable to read your input. "
                              "Please re-attempt or change your embed command."
            )
        elif isinstance(error, commands.errors.UnexpectedQuoteError):
            # An exception raised when the parser encounters a quote mark inside a non-quoted string.
            # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.ArgumentParsingError
            await ctx.send(
                out_message
                + "The parser read a quotation mark where one was not expected. "
                  "Please check the embed command for unnecessary quotation marks."
            )
        elif isinstance(error, commands.errors.InvalidEndOfQuotedStringError):
            # An exception raised when a space is expected after the closing quote in a string but a different char is found.
            # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.ArgumentParsingError
            await ctx.send(
                out_message
                + "The parser expected a space after the closing quote in the embed command, "
                  "but a different character was found."
            )
        elif isinstance(error, commands.errors.ExpectedClosingQuoteError):
            # An exception raised when a quote is expected but not found.
            # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.ArgumentParsingError
            await ctx.send(
                out_message + "The parser expected an end-quote, but it was not found."
            )
        elif isinstance(error, commands.errors.BadArgument):
            # Exception raised when parsing or conversion failure is encountered on an argument to pass into a command.
            # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.UserInputError
            await ctx.send(
                out_message
                + "An exception was raised when parsing due to an invalid argument to the "
                  "embed command."
            )
        elif isinstance(error, commands.errors.TooManyArguments):
            # An exception raised when the command was passed too many arguments.
            # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.UserInputError
            await ctx.send(
                out_message + "Too many arguments were passed to the embed command."
            )
        elif (
                isinstance(error, commands.errors.MissingPermissions)
                or isinstance(error, commands.errors.MissingRole)
                or isinstance(error, commands.errors.MissingAnyRole)
        ):
            # An exception raised when the command invoker lacks admin permissions.
            # https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.CheckFailure
            await ctx.send("Only admin users are permitted to execute embed commands.")
        elif error.args[0].startswith("Command raised an exception: ValueError: Invalid emoji entered to the embed() command"):
            await ctx.send(str(error))
        else:
            # Unknown exception raised.
            await ctx.send(
                out_message
                + "THIS IS AN UNKNOWN ERROR! CONTACT THE TECHNICAL TEAM IMMEDIATELY.\n\t"
                  "ERROR: " + str(error)
            )

    @commands.command
    @commands.has_role(int(os.getenv("MAIN_ADMIN_ROLE")))
    async def help(self, ctx):
        """
        Embed Creation Command:
            /embed <channel category name> <channel header> <reaction emoji> <description in initial embed>
        Note:
            The first two parameters must be one word, or have zero spaces.
            The third parameter must be a valid emoji.
            The last parameter can be however long you want it to be.
        """
        embed = discord.Embed(
            title="Admin Commands Help",
            url="https://hackrpi.com/",
            description="A representative will be with you shortly. If your case can be closed, "
                        "react to this message with the :lock: emoji, and the channel will be "
                        "deleted.",
            color=0x8E2D25,
        )
        await ctx.send(embed=embed)

    # Expo Server helper function for expo channel creation
    @commands.command()
    
    @commands.has_role(int(os.getenv("EXPO_ADMIN_ROLE")))
    async def expo(self, ctx, category_channel_name, text_channel_name, voice_channel_name, low_bound_num, high_bound_num):
        #NOTE TEST command: /expo team- team team 1 3
        await ctx.message.delete()  # immediately deletes original command from chat
        #TODO: Error check expo arguments

        #! create a set of channels (category with text channel + voice channel)
        # adds 1 to high_bound to be inclusive
        for i in range(int(low_bound_num), int(high_bound_num) + 1 ):
            name = category_channel_name + str(i)
            # creates guild
            guild = ctx.message.guild

            #! creates a role for each of the set of channels
            # create role
            team_role = await guild.create_role(name="Team "+str(i))

            # permissions
            overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            team_role: discord.PermissionOverwrite(read_messages=True) # !imp adds team permissions 
            }

            new_category = await ctx.guild.create_category(name, overwrites=overwrites) 
            
            # create text channel
            await guild.create_text_channel("{}-{}-text".format(text_channel_name, str(i)), category=new_category ,
                overwrites=overwrites)
            # create voice channel
            await guild.create_voice_channel("{}-{}-voice".format(voice_channel_name, str(i)), category=new_category,  
                overwrites=overwrites) 
    # end of /expo command

    # Expo server on_member_join
    async def in_hackrpi(self, member_id): 
        # get expo server guild
        guild = self.bot.get_guild(self.EXPO_SERVER) 
 
        # get main HackRPI server guild
        main_guild = self.bot.get_guild(self.MAIN_SERVER) 
        MAIN_JUDGES = main_guild.get_role(self.MAIN_JUDGE_ROLE)
        MAIN_ATTENDEES = main_guild.get_role(self.MAIN_ATTENDEE_ROLE)
 
        #! check main hackrpi server for JUDGE role
        if any(m.id == member_id for m in MAIN_JUDGES.members):
            # apply respective role
            judge_role = guild.get_role(self.EXPO_JUDGE_ROLE)
            user = guild.get_member(member_id)
            await user.add_roles(judge_role)
            #! check main hackrpi server for ATTENDEE role
        elif any(m.id == member_id for m in MAIN_ATTENDEES.members): 
            # apply respective role
            attend_role = guild.get_role(self.EXPO_ATTENDEE_ROLE)
            user = guild.get_member(member_id)
            await user.add_roles(attend_role)
        '''NOTE For additional roles: add constant role ID at top of bot class
           copy and paste if statement snippet above and edit for Sponsor (Specific) role or HackRPI role''' 

    @commands.Cog.listener()
    async def on_member_join(self, member):  
        if member.guild.id == self.EXPO_SERVER:
            await self.in_hackrpi(member.id)
    # end of on_member_join expo server role assignment

# Driver
bot = commands.Bot(command_prefix='/', description='Test bot', intents=intents)
bot.add_cog(TestCog(bot))
bot.run(os.getenv("BOT_TOKEN"), reconnect=True)
