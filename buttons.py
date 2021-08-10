import discord
import channel_actions


class TicketCreationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCreationButton())
        self.add_item(WebsiteButton())


class TicketDeletionView(discord.ui.View):
    def __init__(self, channel_id):
        super().__init__(timeout=None)
        self.channel_id = channel_id
        self.add_item(TicketDeletionButton(channel_id))
        self.add_item(WebsiteButton())


class TicketCreationButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="OPEN TICKET", style=discord.ButtonStyle.blurple, custom_id="ticket_creation_button")

    async def callback(self, interaction: discord.Interaction):
        ticket_name = await channel_actions.create_help_channel(self, interaction)
        interaction_response_embed = discord.Embed(description="The ticket '" + ticket_name + "' has been opened for"
                                                               " you. Please check your list of channels to find it.")
        await interaction.response.send_message(embed=interaction_response_embed, ephemeral=True)


class TicketDeletionButton(discord.ui.Button):
    def __init__(self, channel_id):
        super().__init__(label="CLOSE TICKET", style=discord.ButtonStyle.danger, custom_id="ticket_deletion_button")
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        await channel_actions.delete_help_channel(interaction, self.channel_id)
        

class WebsiteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="OUR WEBSITE", style=discord.ButtonStyle.url, url="https://hackrpi.com/")