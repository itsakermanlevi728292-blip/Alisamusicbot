from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SHUKLAMUSIC import app

# Owner Details Configuration
OWNER_NAME = "Shivansh"
OWNER_USERNAME = "YourTelegramUsername"  # Bina @ ke
OWNER_ID = "8891769246"  # Aapka Telegram User ID
OWNER_BIO = "Music Bot Creator & Developer ⚡"

@app.on_message(filters.command(["rose"]))
async def rose_owner_info(client, message: Message):
    caption = f"""
<emoji id="5431455325206306383">🌹</emoji> <b><u>OWNER DETAILS & PROFILE</u></b> <emoji id="5431455325206306383">🌹</emoji>

<emoji id="5359492143093291241">👤</emoji> <b>Name:</b> {OWNER_NAME}
<emoji id="5431835730384218386">🆔</emoji> <b>User ID:</b> <code>{OWNER_ID}</code>
<emoji id="5431718224206202410">💬</emoji> <b>Username:</b> @{OWNER_USERNAME}
<emoji id="5431375254130168393">📝</emoji> <b>Bio:</b> {OWNER_BIO}

<emoji id="5431520286083341812">✨</emoji> <i>For any queries, bot setup, or support, feel free to contact using the buttons below!</i>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🌹 Contact Owner", url=f"https://t.me/{OWNER_USERNAME}"),
                InlineKeyboardButton("👨‍💻 GitHub", url="https://github.com/itsakermanlevi728292-blip")
            ],
            [
                InlineKeyboardButton("💬 Support Group", url="https://t.me/YourSupportGroup")
            ]
        ]
    )

    await message.reply_text(
        text=caption,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=buttons
    )
    
