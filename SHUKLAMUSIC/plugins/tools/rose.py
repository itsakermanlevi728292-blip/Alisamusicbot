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
# PREMIUM / CUSTOM EMOJI
# Replace this ID with your own custom emoji ID if needed.
# ═══════════════════════════════════════

PREMIUM_EMOJI_ID = "6269180384047533905"

E_CROWN = f'<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">👑</tg-emoji>'
E_STAR = f'<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">✨</tg-emoji>'
E_ROSE = f'<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">🌹</tg-emoji>'
E_ID = f'<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">🆔</tg-emoji>'
E_CHAT = f'<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">💬</tg-emoji>'
E_NOTE = f'<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📝</tg-emoji>'


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

Contact the owner using the buttons
below for bot setup, support & queries.
"""

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

    try:
        await message.reply_text(
            text=text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=buttons
        )

    except Exception as e:
        print(f"[ROSE ERROR] {e}")

        try:
            await message.reply_text(
                f"❌ <b>Rose Command Error</b>\n\n"
                f"<code>{str(e)[:500]}</code>",
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            pass
            
