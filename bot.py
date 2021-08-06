import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
import channel_actions
import buttons
import base64_encoding as b64
import error_checking as err


load_dotenv()
debug_mode = True


class TestCog(commands.Cog):
    def __init__(self, parameter_bot):
        self.bot = parameter_bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Running...")
        self.bot.add_view(buttons.TicketCreationView())

    # !on reaction
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):  # called when a user reacts
    #     if payload.user_id == bot.user.id:  # Prevent the chat log from being sent to the admin channel before deletion
    #         return
    #     channel = bot.get_channel(payload.channel_id)  # get channel id from payload
    #     message = await channel.fetch_message(payload.message_id)  # get message id from payload
    #
    #     if len(message.embeds) != 0 and message.author.id == bot.user.id:
    #         embed = message.embeds[0]  # get the embed from the message
    #         footer = b64.decode(embed.footer.text)
    #
    #         # Searches footer["type"] for channel type (help / sponsor specific / delete)
    #         # Check to see the message is from the bot and it is actually an embed message
    #         if footer["type"] == "HELP_DESK":
    #             await channel_actions.create_help_channel(self, payload, bot)
    #         elif footer["type"] == "DELETE_HELP_CHANNEL":
    #             await channel_actions.delete_help_channel(self, payload, bot)

    # TODO: potentially look into being able to edit the description for the created ticket section
    # TODO: change channel_category to be an ID to an existing category, and update it in create_help_channel when searching
    @commands.command()
    # TODO: use a role by ID from the .env file
    @commands.has_role("admin")
    async def embed(self, ctx, channel_category, custom_ticket, *, text):  # asterisk allows for paragraph input
        # err.embed_error_check(channel_category, custom_ticket, user_reaction, text, bot)

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

        ticket_creation_view = buttons.TicketCreationView()
        await ctx.send(file=file, embed=embed, view=ticket_creation_view)

        # Checks if category already exists and creates the category if it doesn't
        found = False
        for category in ctx.message.guild.categories:
            if str(channel_category) == str(category):
                found = True
                break
        if not found:
            await ctx.guild.create_category(channel_category)

        await ctx.message.delete()

    @embed.error
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
        if debug_mode:
            raise error

    @commands.command
    @commands.has_role("admin")
    async def help(self, ctx):
        """
        Embed Creation Command:
            /embed <channel category name> <channel header> <description in initial embed>
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


# Driver
bot = commands.Bot(command_prefix='/', description='Test bot')
bot.add_cog(TestCog(bot))
bot.run(os.getenv("BOT_TOKEN"), reconnect=True)
