import discord
import channel_actions


class TicketCreationButton(discord.ui.View):
    @discord.ui.button(label="OPEN TICKET", style=discord.ButtonStyle.blurple)
    async def create_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        await channel_actions.create_help_channel(self, interaction)