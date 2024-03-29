import discord
import base64_encoding as b64
import pytz
import buttons
import os


async def create_help_channel(interaction, bot):
    user = interaction.user
    guild = interaction.guild
    message = interaction.message
    embed = message.embeds[0]
    encoded_message = embed.footer.text
    footer = b64.decode(encoded_message)

    print("Channel created for {}".format(user.name))

    # split and parse footer by semi colon (;)
    category_name = footer["category"]
    custom_ticket_name = footer["custom_ticket"]
    ticket_num = footer["ticket_num"]
    ticket_num += 1

    # !imp privacy overwrites
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        # admin user permissions (add admin role and set permissions for more helpers)
        user: discord.PermissionOverwrite(read_messages=True)  # !imp adds user permissions
    }

    category = discord.utils.get(guild.categories, name=category_name)
    # !creates channel inside of category

    ticket_name = "{}-{:04d}".format(custom_ticket_name, ticket_num)
    new_channel = await guild.create_text_channel(
        ticket_name,
        category=category,
        overwrites=overwrites,
    )

    # # remove emoji after channel creation:
    # await message.remove_reaction(payload.emoji.name, user)  # remove user's emoji reaction

    """Get info from embed footer
       if (footer text = delete_help_channel): delete user channel on reaction
       if (footer text = help_channel): create user channel (above) on reaction"""
    # !create new embed in user's channel
    # for customized title, create argument for title, and pass argument into title=
    ticket_embed = discord.Embed(
        title="We are happy to assist you!",
        url="https://hackrpi.com/",
        description="A representative will be with you shortly. If your case can be closed, "
                    "press the \"CLOSE TICKET\" button and the channel will be deleted.",
        color=0x8E2D25,
    )
    file = discord.File("assets/f20logo.png", filename="f20logo.png")
    ticket_embed.set_thumbnail(url="attachment://f20logo.png")

    ticket_deletion_view = buttons.TicketDeletionView(bot)

    '''Set footer'''
    delete_footer = dict()
    delete_footer["type"] = "DELETE_HELP_CHANNEL"
    delete_footer["category"] = category_name
    delete_footer_string = b64.encode(delete_footer)
    ticket_embed.set_footer(text=delete_footer_string)

    await new_channel.send(file=file, embed=ticket_embed, view=ticket_deletion_view)

    new_footer = footer.copy()
    new_footer["ticket_num"] = ticket_num
    new_footer_string = b64.encode(new_footer)  # this is a string

    new_help_desk_embed = discord.Embed(title=embed.title, description=embed.description, color=embed.color)
    new_help_desk_embed.set_thumbnail(url="attachment://f20logo.png")
    new_help_desk_embed.set_footer(text=new_footer_string)
    await message.edit(embed=new_help_desk_embed)

    return ticket_name


async def chat_history(channel, bot):
    users = set()
    with open(f"{channel.name}.txt", "w") as file:
        async for message in channel.history(oldest_first=True):
            # Adjust time for daylight savings
            time_zone = pytz.timezone("US/Eastern")
            if time_zone.dst == 0:
                adjustment = -5
            else:
                adjustment = -4

            '''Generate timestamp'''
            hour = int(message.created_at.hour + adjustment)
            if hour < 0:
                hour = str(24 + hour)
            minute = str(message.created_at.minute)
            if int(minute) < 10:
                minute = "0" + str(minute)
            second = str(message.created_at.second)
            if int(second) < 10:
                second = "0" + str(second)
            time = str(hour) + ":" + str(minute) + ":" + str(second)

            '''Retrieve author username'''
            user = message.author
            users.add(user)
            member = await message.guild.fetch_member(user.id)
            nickname = member.display_name

            '''Append message to transcript'''
            if str(message.content) != "":
                file.write("[" + time + "] " + nickname + ":    " + str(message.content) + "\n")

    file.close()
    ticket_tracker_id = int(os.getenv("TICKET_TRACKER_CHANNEL"))
    tracker_channel = bot.get_channel(ticket_tracker_id)  # Hard-code the administrator channel ID into this operation

    '''Send channel transcript'''
    if len(users) > 0:
        await tracker_channel.send(channel.name, file=discord.File(f"{channel.name}.txt"))  # Send to admin channel
        for user in users:  # Send to all users in channel
            if not user.bot:
                print(f"Closing channel {channel.name}, send to {nickname, user.name, user.id}")
                await user.send(f"Hey {nickname}! Here's a record of your conversation in {channel.name}.",
                                file=discord.File(f"{channel.name}.txt"))  # Send to user
    else:  # No users typed in chat -> Don't send transcript.
        await tracker_channel.send(f"{channel.name} was closed with no conversation.")  # Send message to admin channel


async def delete_help_channel(interaction, bot):
    channel = interaction.channel
    await chat_history(channel, bot)  # Send transcript to tracker channel
    await channel.delete()  # Delete the ticket channel
