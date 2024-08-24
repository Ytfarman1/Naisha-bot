import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from DAXXMUSIC import userbot as us, app
from DAXXMUSIC.core.userbot import assistants

@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    if len(message.text.split()) < 2 and not message.reply_to_message:
        return await message.reply("Please provide a username, ID, or reply to a user.")
    
    if message.reply_to_message:
        args = message.reply_to_message.from_user.id
    else:
        args = message.text.split()[1]

    lol = await message.reply("<code>Processing...</code>")
    
    try:
        user = await client.get_users(args)
    except Exception:
        return await lol.edit("<code>Please specify a valid user!</code>")
    
    bot_choice = random.choice(["sangmata_bot", "sangmata_beta_bot"])
    
    # Check if assistant is available
    if 1 in assistants:
        ubot = us.one
    else:
        return await lol.edit("<code>No assistant is available.</code>")
    
    try:
        a = await ubot.send_message(bot_choice, str(user.id))
        await a.delete()
    except Exception as e:
        return await lol.edit(str(e))
    
    await asyncio.sleep(1)  # Adjust if necessary
    
    async for stalk in ubot.search_messages(bot_choice, limit=10):
        if stalk and stalk.text:
            await message.reply(stalk.text)
            break
    else:
        await message.reply("No response received from the bot.")
    
    try:
        user_info = await ubot.resolve_peer(bot_choice)
        await ubot.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception as e:
        pass
    
    await lol.delete()
