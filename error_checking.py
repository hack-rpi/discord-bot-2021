import discord
import emoji


def check_emoji(_emoji, bot):
    if len(_emoji) > 1 and '<' == _emoji[0] and '>' == _emoji[-1] and ':' in _emoji:  # Custom discord emoji detected
        # Unicode emojis only have ':' no '<' '>'
        emote_name = _emoji.split(':')[1]  # Retrieve the emoji name
        for server in bot.guilds:  # Search all servers the bot is in
            for emote in server.emojis:  # Search all emojis in all servers the bot is in
                if emote.name == emote_name and discord.Emoji.is_usable(emote):
                    # Discord bots have Nitro privileges for emojis -- Can use custom emojis from other servers
                    return True, emote  # Bot is able to use the custom emoji
        return False, "emoji"  # Bot is unable to use the provided emoji

    emoji_name = emoji.demojize(_emoji)  # Generate Unicode emoji name
    if emoji_name != _emoji:  # Checks to make sure a custom emoji hasn't demojized to Unicode
        return True, _emoji


def embed_error_check(channel_category, custom_ticket, user_reaction, text, bot):
    is_emoji, emoji_response = check_emoji(user_reaction, bot)
    if not is_emoji:
        msg = f"Invalid emoji entered to the embed() command: \"{user_reaction}\"\n\tPlease choose a different emoji."
        raise ValueError(msg)

    returned_error = "NO_ERROR"
    if not isinstance(channel_category, str):
        returned_error = "channel string"
    elif not isinstance(custom_ticket, str):
        returned_error = True, "ticket string"
    elif not isinstance(text, str):
        returned_error = True, "text string"

    if returned_error != "NO_ERROR":
        raise ValueError(f"Invalid input to embed() command for the {returned_error}.")

