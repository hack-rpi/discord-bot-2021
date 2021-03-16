Scope and Concept: 

3/8 Task:
    When a message is reacted to by a user (non-bot), create a new text channel (with the channel category as one of the bot arguments)
    add the the user who reacted to the bot message, to the new channel
    Future: 
    grab text from post and look into storing meta data on post 
    Tip: Encode info into json object, base 64, footer area  

Test Bot Purpose:
    On submit, the bot creates a post with a reaction in the current channel 
     /create    Channel category        Reaction        Text

LATEST 3/6 Working test case for embed
    /embed general :thumbsup: hello world

    Note: :thumbsup: is an emoji (all emojis universally compatible at https://emojipedia.org/)

3/5 Working test case with emoji:
    /create general :thumbsup: hello world 

    Note: :thumbsup: is an emoji (all emojis universally compatible at https://emojipedia.org/)