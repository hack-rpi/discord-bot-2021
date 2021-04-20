Scope and Concept: 

LATEST: 4/19 Task:
    1. Add ticket counter to each embed footer
        Store counter in general (envelope) embed footer 
    2. Including the option for a custom name 
    add IBM optional argument before embed description: 
         /embed HELP_DESK :envelope_with_arrow: IBM Any questions? React with :envelope_with_arrow: to get them answered! 
    Rather than only having ticket-1:
      Ticket-2
      IBM-2
      TroyWeb-4
    3. Embed ticket counter into the message (embed) footer 
        Parse, Update (increment) ticket count in the embed footer
    4. When a channel is deleted, send a HTML message to the user with the channel contents 
        In the future: Send HTML channel contents to HackRPI admin channel

4/5 Task: COMPLETE by Charles (4/17)
    Test case:  /embed HELP_DESK :envelope_with_arrow: Any questions? React with :envelope_with_arrow: to get them answered!
    
    Within the user's new channel, create an embed with a reaction
    When a user reacts with the reaction, the channel will be deleted.

    This task also included adding the channel type to the footer of the embed, 
    so the on_raw_reaction_add function can be fully functional for different on_ reaction tasks

    Grab the footer channel type: 
    if embed footer type == help_channel, then initialize help channel
    else if embed footer type == delete_channel, then delete channel

3/31 Task: COMPLETE by Bryce
    /embed HELP_DESK :envelope_with_arrow: Any questions? React with :envelope_with_arrow: to get them answered!

    -> WITH on_raw_reaction(self, payload) <-
    
    When a message is reacted to by a user (non-bot), create a new text channel (with the channel category as one of the bot arguments)
    add the the user who reacted to the bot message, to the new channel
    Deletes user's reaction after private channel initialization and user move
    Future: 
        grab text from post and look into storing meta data on post 
        Tip: Encode info into json object, base 64, footer area  

3/8 Task: COMPLETE by Bryce
    /embed HELP_DESK :envelope_with_arrow: Any questions? React with :envelope_with_arrow: to get them answered!
    
    When a message is reacted to by a user (non-bot), create a new text channel (with the channel category as one of the bot arguments)
    add the the user who reacted to the bot message, to the new channel
    Future: 
    grab text from post and look into storing meta data on post 
    Tip: Encode info into json object, base 64, footer area  

    Test Bot Purpose:
        On submit, the bot creates a post with a reaction in the current channel 
        /create    Channel category        Reaction        Text

3/6 Working test case for embed: COMPLETE by Bryce
    /embed general :thumbsup: hello world

    Note: :thumbsup: is an emoji (all emojis universally compatible at https://emojipedia.org/)

3/5 Working test case with emoji: COMPLETE by Bryce
    /create general :thumbsup: hello world 

    Note: :thumbsup: is an emoji (all emojis universally compatible at https://emojipedia.org/)