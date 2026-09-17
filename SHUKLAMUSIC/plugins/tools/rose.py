from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from SHUKLAMUSIC import app

# Owner Details
OWNER_NAME = "ටිαѕυкє"
OWNER_USERNAME = "sasuke_qt"
OWNER_ID = "8672927645"
OWNER_BIO = "𝐅ʀᴏᴍ 𝐒ᴜғғᴇʀɪɴɢ 𝐂ᴏᴍᴇs 𝐆ʟᴏʀʏ"

# Image URL (Aapki Sasuke photo ka direct link)
# Agar link badalna ho to photo ko kisi TG channel/bot par bhej kar link copy karke yahan replace karein
IMAGE_URL = "https://telegra.ph/file/0db447d91e3271424750f.jpg" 

# 18-digit Telegram Premium Emoji ID
PREMIUM_EMOJI_ID = "5431520286083341812"

@app.on_message(filters.command(["rose"]))
async def rose_owner_info(client, message: Message):
    caption = f"""
<emoji id="{PREMIUM_EMOJI_ID}">🌹</emoji> <b><u>OWNER DETAILS & PROFILE</u></b> <emoji id="{PREMIUM_EMOJI_ID}">🌹</emoji>

<emoji id="{PREMIUM_EMOJI_ID}">👤</emoji> <b>Name:</b> <a href="tg://openmessage?user_id={OWNER_ID}">{OWNER_NAME}</a>
<emoji id="{PREMIUM_EMOJI_ID}">🆔</emoji> <b>User ID:</b> <code>{OWNER_ID}</code>
<emoji id="{PREMIUM_EMOJI_ID}">💬</emoji> <b>Username:</b> @{OWNER_USERNAME}
<emoji id="{PREMIUM_EMOJI_ID}">📝</emoji> <b>Bio:</b> {OWNER_BIO} <emoji id="{PREMIUM_EMOJI_ID}">⚡</emoji>

<emoji id="{PREMIUM_EMOJI_ID}">✨</emoji> <i>Click buttons below to interact!</i>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🌹 Contact Owner (Primary)", url=f"https://t.me/{OWNER_USERNAME}"),
            ],
            [
                InlineKeyboardButton("✨ Share Owner Info (Success Style)", switch_inline_query="owner"),
            ],
            [
                InlineKeyboardButton("⚠️ Warning / Rules (Danger Alert)", callback_data="rose_danger_alert"),
            ]
        ]
    )

    # Simple Text Message ki jagah Photo ke sath Caption bhej rahe hain
    await message.reply_photo(
        photo=IMAGE_URL,
        caption=caption,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("rose_danger_alert"))
async def danger_callback(client, callback_query: CallbackQuery):
    await callback_query.answer(
        "🚨 DANGER / ALERT ZONE 🚨\n\nUnauthorized spamming or abuse will result in a permanent ban!",
        show_alert=True
)

