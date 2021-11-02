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


class TicketDeletionConfirmationView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        confirm_label = "Yes, close the ticket"
        cancel_label = "No, keep the ticket open"
        self.add_item(CancellationButton(cancel_label))
        self.add_item(ConfirmationButton(confirm_label, channel_actions.delete_help_channel, bot,
                                         need_interaction=True))


class TicketCreationButton(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(label="OPEN TICKET", style=discord.ButtonStyle.blurple, custom_id="ticket_creation_button")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        ticket_name = await channel_actions.create_help_channel(interaction, self.bot)
        interaction_response_embed = discord.Embed(description="The ticket '" + ticket_name + "' has been opened for "
                                                                                              "you. Please check your "
                                                                                              "list of channels to "
                                                                                              "find it.")
        await interaction.response.send_message(embed=interaction_response_embed, ephemeral=True)


class TicketDeletionButton(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(label="CLOSE TICKET", style=discord.ButtonStyle.red, custom_id="ticket_deletion_button")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        delete_ticket_confirmation_view = TicketDeletionConfirmationView(self.bot)
        confirmation_message = "Are you sure you want to close your current ticket? This action is not reversible."
        confirmation_embed = discord.Embed(description=confirmation_message)
        await interaction.channel.send(view=delete_ticket_confirmation_view, embed=confirmation_embed,
                                       delete_after=10)


class WebsiteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="OUR WEBSITE", style=discord.ButtonStyle.url, url="https://hackrpi.com/")


class ConfirmationButton(discord.ui.Button):
    def __init__(self, label, function, *args, need_interaction=False):
        super().__init__(label=label, style=discord.ButtonStyle.gray, custom_id="confirmation_button")
        self.need_interaction = need_interaction
        self.function = function
        self.arguments = []
        for arg in args:
            self.arguments.append(arg)

    async def callback(self, interaction: discord.Interaction):
        if self.need_interaction:
            if inspect.iscoroutinefunction(self.function):
                await self.function(interaction, *self.arguments)
            else:
                self.function(interaction, *self.arguments)
        else:
            if inspect.iscoroutinefunction(self.function):
                await self.function(*self.arguments)
            else:
                self.function(*self.arguments)


class CancellationButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.red, custom_id="cancellation_button")

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
