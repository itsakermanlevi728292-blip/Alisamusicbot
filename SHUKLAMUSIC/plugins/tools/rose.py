from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from SHUKLAMUSIC import app


# ═══════════════════════════════════════
# OWNER CONFIG
# ═══════════════════════════════════════

OWNER_NAME = "SASUKE"
OWNER_USERNAME = "sasuke_qt"
OWNER_ID = 8672927645
OWNER_BIO = "𝐅ʀᴏᴍ 𝐒ᴜғғᴇʀɪɴɢ 𝐂ᴏᴍᴇs 𝐆ʟᴏʀʏ ⚡"


# ═══════════════════════════════════════
# PREMIUM EMOJI
# ═══════════════════════════════════════

E_CROWN = '<tg-emoji emoji-id="6269180384047533905">👑</tg-emoji>'
E_STAR = '<tg-emoji emoji-id="6269180384047533905">✨</tg-emoji>'
E_ROSE = '<tg-emoji emoji-id="6269180384047533905">🌹</tg-emoji>'
E_ID = '<tg-emoji emoji-id="6269180384047533905">🆔</tg-emoji>'
E_CHAT = '<tg-emoji emoji-id="6269180384047533905">💬</tg-emoji>'
E_NOTE = '<tg-emoji emoji-id="6269180384047533905">📝</tg-emoji>'


# ═══════════════════════════════════════
# /ROSE COMMAND
# ═══════════════════════════════════════

@app.on_message(
    filters.command(
        ["rose"],
        prefixes=["/", "!", "."]
    )
)
async def rose_owner_info(client, message: Message):

    text = f"""
{E_ROSE} <b>OWNER DETAILS & PROFILE</b> {E_ROSE}

{E_CROWN} <b>Name:</b>
<a href="tg://user?id={OWNER_ID}">{OWNER_NAME}</a>

{E_ID} <b>User ID:</b>
<code>{OWNER_ID}</code>

{E_CHAT} <b>Username:</b>
@{OWNER_USERNAME}

{E_NOTE} <b>Bio:</b>
<i>{OWNER_BIO}</i>

━━━━━━━━━━━━━━━━━━

{E_STAR} <b>Need Help or Support?</b>

Contact the owner using the button
below for bot setup, support & queries.
"""


    # ═══════════════════════════════════
    # PREMIUM BUTTONS
    # ═══════════════════════════════════

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🌹 ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ",
                    url=f"https://t.me/{OWNER_USERNAME}"
                )
            ],
            [
                InlineKeyboardButton(
                    "✨ ᴍʏ ᴄʜᴀɴɴᴇʟ",
                    url="https://t.me/Aw_Music_channel"
                )
            ]
        ]
    )


    # ═══════════════════════════════════
    # SEND MESSAGE
    # ═══════════════════════════════════

    try:

        await message.reply_text(
            text=text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=buttons,
            disable_web_page_preview=True
        )

    except Exception as e:

        print(f"[ROSE ERROR] {e}")

        await message.reply_text(
            f"❌ <b>Rose Command Error</b>\n\n"
            f"<code>{str(e)[:500]}</code>",
            parse_mode=enums.ParseMode.HTML
    )
