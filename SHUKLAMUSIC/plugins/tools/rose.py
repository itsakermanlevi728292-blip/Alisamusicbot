from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from SHUKLAMUSIC import app

# Configuration
OWNER_NAME = "ටිαѕυкє"
OWNER_USERNAME = "sasuke_qt"
OWNER_ID = "8672927645"
OWNER_BIO = "𝐅ʀᴏᴍ 𝐒ᴜғғᴇʀɪɴɢ 𝐂ᴏᴍᴇs 𝐆ʟᴏʀʏ ⚡"

@app.on_message(filters.command(["rose", "Rose"], prefixes=["/", "!", "."]))
async def rose_owner_info(client, message: Message):
    caption = f"""
🌹 <b><u>OWNER DETAILS & PROFILE</u></b> 🌹

👤 <b>Name:</b> <a href="tg://user?id={OWNER_ID}">{OWNER_NAME}</a>
🆔 <b>User ID:</b> <code>{OWNER_ID}</code>
💬 <b>Username:</b> @{OWNER_USERNAME}
📝 <b>Bio:</b> {OWNER_BIO}

✨ <i>For any queries, bot setup, or support, feel free to contact using the buttons below!</i>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🌹 Contact Owner", url=f"https://t.me/{OWNER_USERNAME}"),
            ],
            [
                InlineKeyboardButton("✨ Share Owner Info", switch_inline_query="owner"),
            ],
            [
                InlineKeyboardButton("⚠️ Warning / Rules", callback_data="rose_danger_alert"),
            ]
        ]
    )

    await message.reply_text(
        text=caption,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("rose_danger_alert"))
async def danger_callback(client, callback_query: CallbackQuery):
    await callback_query.answer(
        "🚨 DANGER / ALERT ZONE 🚨\n\nUnauthorized spamming or abuse will result in a permanent ban!",
        show_alert=True
    )
    
