import discord
from discord.ext import commands
import json


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
        ticketNumber = 0
        if len(embed.footer.text[10:]) != 0:
            ticketNumber = int(embed.footer.text[10:])
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
        ticketEmbed.set_footer(text="DELETE_HELP_CHANNEL")  # add category to embed footer
        channel = discord.utils.get(guild.channels, name="ticket-{:04d}".format(ticketNumber))
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        ticketMessage = await channel.send(file=file, embed=ticketEmbed)
        await ticketMessage.add_reaction("🔒")

        newFooter = embed.footer.text[:9] + "_{:02d}".format(ticketNumber)
        newHelpDeskEmbed = discord.Embed(title=embed.title, description=embed.description, color=embed.color)
        file = discord.File("assets/f20logo.png", filename="f20logo.png")
        newHelpDeskEmbed.set_thumbnail(url="attachment://f20logo.png")
        # newHelpDeskEmbed.set_thumbnail(url=embed.thumbnail.url)
        newHelpDeskEmbed.set_footer(text=newFooter)
        await message.edit(embed=newHelpDeskEmbed)


async def delete_help_channel(self, payload, bot):
    user = await self.bot.fetch_user(payload.user_id)
    if user != bot.user:
        channel = bot.get_channel(payload.channel_id)  # get channel id from payload
        await channel.delete()
