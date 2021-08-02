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

    async def create_ticket(self, interaction: discord.Interaction):
        await channel_actions.create_help_channel(self, interaction)


class WebsiteButton(discord.ui.Button["website"]):
    def __init__(self):
        super().__init__(label="OUR WEBSITE", style=discord.ButtonStyle.url, url="https://hackrpi.com/")