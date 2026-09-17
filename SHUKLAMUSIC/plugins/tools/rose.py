from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SHUKLAMUSIC import app

# Configuration
OWNER_NAME = "ටිαѕυкє"
OWNER_USERNAME = "sasuke_qt"
OWNER_ID = 8672927645
OWNER_BIO = "𝐅ʀᴏᴍ 𝐒ᴜғғᴇʀɪɴɢ 𝐂ᴏᴍᴇs 𝐆ʟᴏʀʏ ⚡"

@app.on_message(filters.command(["rose", "Rose"], prefixes=["/", "!", "."]))
async def rose_owner_info(client, message: Message):
    text = f"""
🌹 <b><u>OWNER DETAILS & PROFILE</u></b> 🌹

👑 <b>Name:</b> <a href="tg://user?id={OWNER_ID}">{OWNER_NAME}</a>
🆔 <b>User ID:</b> <code>{OWNER_ID}</code>
💬 <b>Username:</b> @{OWNER_USERNAME}
📝 <b>Bio:</b> {OWNER_BIO}

✨ <i>For any queries, bot setup, or support, click the buttons below!</i>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🌹 Contact Owner", url=f"https://t.me/{OWNER_USERNAME}"),
            ],
            [
                InlineKeyboardButton("✨ Share Info", switch_inline_query="owner"),
            ]
        ]
    )

    await message.reply_text(
        text=text,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=buttons,
        disable_web_page_preview=True
    )
    
