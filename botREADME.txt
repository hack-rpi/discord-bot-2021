Scope and Concept: 

4/5 Task:
    Within the user's new channel, create an embed with a reaction
    When a user reacts with the reaction, the channel will be deleted.

    This task also included adding the channel type to the footer of the embed, 
    so the on_raw_reaction_add function can be fully functional for different on_ reaction tasks

    Grab the footer channel type: 
    if embed footer type == help_channel, then initialize help channel
    else if embed footer type == delete_channel, then delete channel

LATEST 3/31 Task: 
    /embed HELP_DESK :envelope_with_arrow: Any questions? React with :envelope_with_arrow: to get them answered!

    -> WITH on_raw_reaction(self, payload) <-
    
    When a message is reacted to by a user (non-bot), create a new text channel (with the channel category as one of the bot arguments)
    add the the user who reacted to the bot message, to the new channel
    Deletes user's reaction after private channel initialization and user move
    Future: 
        grab text from post and look into storing meta data on post 
        Tip: Encode info into json object, base 64, footer area  

3/8 Task:
    /embed HELP_DESK :envelope_with_arrow: Any questions? React with :envelope_with_arrow: to get them answered!
    
    When a message is reacted to by a user (non-bot), create a new text channel (with the channel category as one of the bot arguments)
    add the the user who reacted to the bot message, to the new channel
    Future: 
    grab text from post and look into storing meta data on post 
    Tip: Encode info into json object, base 64, footer area  

    Test Bot Purpose:
        On submit, the bot creates a post with a reaction in the current channel 
        /create    Channel category        Reaction        Text

3/6 Working test case for embed
    /embed general :thumbsup: hello world

    Note: :thumbsup: is an emoji (all emojis universally compatible at https://emojipedia.org/)

3/5 Working test case with emoji:
    /create general :thumbsup: hello world 

    Note: :thumbsup: is an emoji (all emojis universally compatible at https://emojipedia.org/)