import discord
from discord.ext import commands
import json
import pytz


async def create_help_channel(self, payload, bot):
    user = await self.bot.fetch_user(payload.user_id)
    if user != bot.user:
        print("Channel created for {}".format(user.name))  # await ctx.send
        # search for current ticket count
        with open("assets/ticketCount.json", "r") as f:
            data = json.load(f)
        ticketNumber = int(data['ticket-counter'])

        # increase count
        ticketNumber += 1

        guild = self.bot.get_guild(payload.guild_id)

        # !imp privacy overwrites
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            # admin user permissions (add admin role and set permissions for more helpers)
            user: discord.PermissionOverwrite(read_messages=True)  # !imp adds user permissions
        }

        # create private ticket text channel  #!imp - hard coded category name
        name = "HELP_DESK"
        # sets category name from command argument
        guild = bot.get_guild(payload.guild_id)

        category = discord.utils.get(guild.categories, name=name)
        categoryFin = category  # stops channels from going public
        # !creates channel inside of category
        print("ticket-{:04d}".format(ticketNumber))
        await guild.create_text_channel("ticket-{:04d}".format(ticketNumber), category=categoryFin,
                                        overwrites=overwrites)

        # remove emoji after channel creation:
        channel = bot.get_channel(payload.channel_id)  # get channel id from payload
        message = await channel.fetch_message(payload.message_id)  # get message id from payload
        await message.remove_reaction(payload.emoji.name, user)  # remove user's emoji reaction

        # update json file with ticket count
        data["ticket-counter"] = ticketNumber
        with open("assets/ticketCount.json", "w") as write_file:
            json.dump(data, write_file)

        '''get info from embed footer
           if (footer text = delete_help_channel): delete user channel on reaction
           if (footer text = help_channel): create user channel (above) on reaction'''
        # !create new embed in user's channel
        # for customized title, create argument for title, and pass argument into title=
        embed = discord.Embed(title="We are happy to assist you!", url="https://hackrpi.com/",
                              description="A representative will be with you shortly. If your case can be closed, react to this message with the :lock: emoji, and the channel will be deleted.",
                              color=0x8E2D25)
        file = discord.File("assets/f20logo.png", filename="f20logo.png")
        embed.set_thumbnail(url="attachment://f20logo.png")
        # set footer
        embed.set_footer(text="DELETE_HELP_CHANNEL")  # add category to embed footer
        channel = discord.utils.get(guild.channels, name="ticket-{:04d}".format(ticketNumber))
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        msg = await channel.send(file=file, embed=embed)

        await msg.add_reaction("🔒")

async def chat_history(channel, payload, bot):
    users = set()
    with open(f"{channel.name}.html", "w") as file:
        async for message in channel.history(oldest_first = True):
            # Adjust time for daylight savings
            timeZone = pytz.timezone("US/Eastern")
            if timeZone.dst == 0:
                adjustment = -5
            else:
                adjustment = -4

            # Generate timestamp
            hour = str(message.created_at.hour + adjustment)
            if int(hour) < 0: hour = str(12 + adjustment)
            if int(hour) == 0: hour = "12"

            minute = str(message.created_at.minute)
            if int(minute) < 10: minute = "0" + str(minute)

            second = str(message.created_at.second)
            if int(second) < 10: second = "0" + str(second)

            time = hour + ":" + minute + ":" + second

            user = message.author
            users.add(user)

            if str(message.content) != "":  # Append message to transcript
                file.write("[" + time + "] " + str(message.author) + ":    " + str(message.content) + "<br>")
    file.close()

    tracker_channel = bot.get_channel(843289182344183869)  # Hard-code the administrator channel ID into this operation

    if len(users) > 0:
        await tracker_channel.send(channel.name, file=discord.File(f"{channel.name}.html"))
        for user in users:
            if not user.bot :
                print(f"Closing channel {channel.name}, send to {user.name, user.id}")
                await user.send(f"Hey {user.name}! Here's a record of your conversation in {channel.name}.", file=discord.File(f"{channel.name}.html"))
    else:
        await tracker_channel.send(f"{channel.name} was closed with no conversation.")

async def delete_help_channel(self, payload, bot):
    channel = bot.get_channel(payload.channel_id)
    await chat_history(channel, payload, bot)  # Generate and send transcript
    user = await self.bot.fetch_user(payload.user_id)
    if user != bot.user:
        channel = bot.get_channel(payload.channel_id)  # get channel id from payload
        await channel.delete()
