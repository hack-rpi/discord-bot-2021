import discord
import channel_actions
import inspect


class TicketCreationView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(TicketCreationButton(bot))
        self.add_item(WebsiteButton())


class TicketDeletionView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(TicketDeletionButton(bot))
        self.add_item(WebsiteButton())


class ConfirmationView(discord.ui.View):
    def __init__(self, bot, confirm_label, cancel_label, function, *args):
        super().__init__(timeout=None)
        self.add_item(CancellationButton(cancel_label))
        self.add_item(ConfirmationButton(confirm_label, function, *args))
        # bot.add_view(self)


class TicketCreationButton(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(label="OPEN TICKET", style=discord.ButtonStyle.blurple, custom_id="ticket_creation_button")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        ticket_name = await channel_actions.create_help_channel(self, interaction, self.bot)
        interaction_response_embed = discord.Embed(description="The ticket '" + ticket_name + "' has been opened for"
                                                                                              " you. Please check your list of channels to find it.")
        await interaction.response.send_message(embed=interaction_response_embed, ephemeral=True)


class TicketDeletionButton(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(label="CLOSE TICKET", style=discord.ButtonStyle.red, custom_id="ticket_deletion_button")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        confirm_label = "Yes, close the ticket"
        cancel_label = "No, keep the ticket open"
        delete_ticket_confirmation_view = ConfirmationView(self.bot, confirm_label, cancel_label,
                                                           channel_actions.delete_help_channel, self,
                                                           interaction, self.bot)
        # self.bot.add_view(delete_ticket_confirmation_view)
        confirmation_message = "Are you sure you want to close your current ticket? This action is not reversible."
        confirmation_embed = discord.Embed(description=confirmation_message)
        await interaction.response.send_message(view=delete_ticket_confirmation_view, embed=confirmation_embed)


class WebsiteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="OUR WEBSITE", style=discord.ButtonStyle.url, url="https://hackrpi.com/")


class ConfirmationButton(discord.ui.Button):
    def __init__(self, label, function, *args):
        super().__init__(label=label, style=discord.ButtonStyle.gray, custom_id="confirmation_button")
        self.function = function
        self.arguments = []
        for arg in args:
            self.arguments.append(arg)

    async def callback(self, interaction: discord.Interaction):
        if inspect.iscoroutinefunction(self.function):
            await self.function(*self.arguments)
        else:
            self.function(*self.arguments)


class CancellationButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.red, custom_id="cancellation_button")

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
