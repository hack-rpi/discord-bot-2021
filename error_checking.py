import discord
import emoji


def check_emoji(_emoji, bot):
    custom_emoji = False
    if len(_emoji) > 1 and '<' == _emoji[0] and '>' == _emoji[-1] and ':' in _emoji:  # Custom discord emoji detected
        # Unicode emojis only have ':' no '<' '>'
        emote_name = _emoji.split(':')[1]  # Retrieve the emoji name
        for server in bot.guilds:  # Search all servers the bot is in
            for emote in server.emojis:  # Search all emojis in all servers the bot is in
                if emote.name == emote_name and discord.Emoji.is_usable(emote):
                    # Discord bots have Nitro privs for emojis -- Can use custom emojis from other servers
                    return True, emote  # Bot is able to use the custom emoji
        return False, "emoji"  # Bot is unable to use the provided emoji

    emoji_name = emoji.demojize(_emoji)  # Generate Unicode emoji name
    if emoji_name == _emoji:  # Custom emojis will not demojize
        return False, "emoji"  # Bot is unable to use the provided emoji
    else:  # Unicode emoji detected
        return True, _emoji


def embed_error_check(channel_category, custom_ticket, user_reaction, text, bot):
    channel_string = isinstance(channel_category, str)
    ticket_string = isinstance(custom_ticket, str)
    text_string = isinstance(text, str)

    is_emoji, emoji_response = check_emoji(user_reaction, bot)

    if not channel_string:
        return True, "channel string"
    elif not ticket_string:
        return True, "ticket string"
    elif not text_string:
        return True, "text string"
    elif not is_emoji:
        return True, "emoji"
    else:  # No errors
        return False, ""
