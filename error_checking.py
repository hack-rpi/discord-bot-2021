import discord


def is_emoji(emoji):
    try:
        if not isinstance(emoji, str) and emoji[0] != '<' and emoji[-1] != '>':
            return False
        lis = emoji[2:-1].split(":")
        if not isinstance(lis[0], str):
            return False
        if not isinstance(lis[1], str) and not lis[1].isnumeric():
            return False
        return True
    except IndexError:
        return False


def embed_error_check(channel_category, custom_ticket, user_reaction, text):
    if not (isinstance(channel_category, str) and isinstance(custom_ticket, str) and is_emoji(user_reaction) and \
            isinstance(text, str)):
        return False
    return True
