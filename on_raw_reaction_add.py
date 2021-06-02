import discord
from discord.ext import commands
import base64_encoding as b64
import json
import pytz


async def create_help_channel(self, payload, bot): 
    user = await self.bot.fetch_user(payload.user_id)
    if user != bot.user:
        print("Channel created for {}".format(user.name))  # await ctx.send
        # search for current ticket count
        # with open("assets/ticketCount.json", "r") as f:
        #     data = json.load(f)
        # ticketNumber = int(data['ticket-counter'])
        #
        # # increase count
        # ticketNumber += 1
        channel = bot.get_channel(payload.channel_id)  # get channel id from payload
        message = await channel.fetch_message(payload.message_id)  # get message id from payload
        embed = message.embeds[0] 
        encodedMessage = embed.footer.text
        footer = b64.decode(encodedMessage)
        
        print("decodedMessage: ", footer)

        # split and parse footer by semi colon (;)
        category_name, custom_ticket_name, ticketNum = footer.split(';')
        # elements[0] = category_name    elements[1] = custom ticket name    elements[2] = ticket 

        currentFooterNum = ticketNum 
        ticketNumber = 0 
        if len(currentFooterNum) != 0:
            ticketNumber = int(currentFooterNum)
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
 
        # print("first: ", currentName+"-{:04d}".format(ticketNumber)) 

        currentName = custom_ticket_name 
        newChannel = await guild.create_text_channel("{}-{:04d}".format(currentName, ticketNumber), category=categoryFin,
                                        overwrites=overwrites)

        # remove emoji after channel creation:
        await message.remove_reaction(payload.emoji.name, user)  # remove user's emoji reaction

        # update json file with ticket count
        # data["ticket-counter"] = ticketNumber
        # with open("assets/ticketCount.json", "w") as write_file:
        #     json.dump(data, write_file)

        '''get info from embed footer
           if (footer text = delete_help_channel): delete user channel on reaction
           if (footer text = help_channel): create user channel (above) on reaction'''
        # !create new embed in user's channel
        # for customized title, create argument for title, and pass argument into title=
        ticketEmbed = discord.Embed(title="We are happy to assist you!", url="https://hackrpi.com/",
                              description="A representative will be with you shortly. If your case can be closed, react to this message with the :lock: emoji, and the channel will be deleted.",
                              color=0x8E2D25)
        file = discord.File("assets/f20logo.png", filename="f20logo.png")
        ticketEmbed.set_thumbnail(url="attachment://f20logo.png")
        # set footer
        ticketEmbed.set_footer(text=b64.encode("DELETE_HELP_CHANNEL"))  # add category to embed footer 
 
        #!imp print test 
        currentName = custom_ticket_name  
        # channel = discord.utils.get(guild.channels, name=newChannel) //original

        channel= newChannel
        print("channel", channel)
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        ticketMessage = await channel.send(file=file, embed=ticketEmbed)
        await ticketMessage.add_reaction("🔒")

        strng = category_name + ';' + custom_ticket_name + ';'

        temp = strng + "{:02d}".format(ticketNumber)
        newFooter = b64.encode(temp)
        newHelpDeskEmbed = discord.Embed(title=embed.title, description=embed.description, color=embed.color)
        file = discord.File("assets/f20logo.png", filename="f20logo.png")
        newHelpDeskEmbed.set_thumbnail(url="attachment://f20logo.png")
        # HelpDeskEmbed.set_thumbnail(url=embed.thumbnail.url)
        newHelpDeskEmbed.set_footer(text=newFooter)
        await message.edit(embed=newHelpDeskEmbed)


async def chat_history(channel, payload, bot):
    users = set()
    with open(f"{channel.name}.txt", "w") as file:
        async for message in channel.history(oldest_first=True):
            # Adjust time for daylight savings
            timeZone = pytz.timezone("US/Eastern")
            if timeZone.dst == 0:
                adjustment = -5
            else:
                adjustment = -4

            # Generate timestamp
            hour = message.created_at.hour + adjustment
            if hour < 0: hour = str(24 + hour)

            minute = str(message.created_at.minute)
            if int(minute) < 10: minute = "0" + str(minute)

            second = str(message.created_at.second)
            if int(second) < 10: second = "0" + str(second)

            time = hour + ":" + minute + ":" + second

            user = message.author
            users.add(user)
            member = await message.guild.fetch_member(user.id)
            nickname = member.display_name

            if str(message.content) != "":  # Append message to transcript
                file.write("[" + time + "] " + nickname + ":    " + str(message.content) + "\n")
    file.close()

    tracker_channel = bot.get_channel(843289182344183869)  # Hard-code the administrator channel ID into this operation

    if len(users) > 0:
        await tracker_channel.send(channel.name, file=discord.File(f"{channel.name}.txt"))
        for user in users:
            if not user.bot:
                print(f"Closing channel {channel.name}, send to {nickname, user.name, user.id}")
                await user.send(f"Hey {nickname}! Here's a record of your conversation in {channel.name}.",
                                file=discord.File(f"{channel.name}.txt"))
    else:
        await tracker_channel.send(f"{channel.name} was closed with no conversation.")


async def delete_help_channel(self, payload, bot):
    channel = bot.get_channel(payload.channel_id)
    await chat_history(channel, payload, bot)  # Generate and send transcript
    user = await self.bot.fetch_user(payload.user_id)
    if user != bot.user:
        channel = bot.get_channel(payload.channel_id)  # get channel id from payload
        await channel.delete()
