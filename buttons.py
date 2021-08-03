import discord
import channel_actions


class TicketCreationView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketCreationButton())
        self.add_item(WebsiteButton())


class TicketCreationButton(discord.ui.Button["ticket_creation"]):
    def __init__(self):
        super().__init__(label="OPEN TICKET", style=discord.ButtonStyle.blurple, custom_id="ticket_creation_button")

    async def callback(self, interaction: discord.Interaction):
        interaction_response_embed = discord.Embed(description="A new ticket has been opened for you. Please check your"
                                                               " list of channels to find it.")
        await interaction.response.send_message(embed=interaction_response_embed, ephemeral=True)
        await channel_actions.create_help_channel(self, interaction)


class WebsiteButton(discord.ui.Button["website"]):
    def __init__(self):
        super().__init__(label="OUR WEBSITE", style=discord.ButtonStyle.url, url="https://hackrpi.com/")