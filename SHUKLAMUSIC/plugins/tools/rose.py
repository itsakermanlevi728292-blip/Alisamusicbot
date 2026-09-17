import httpx

from pyrogram import filters
from pyrogram.types import Message

from SHUKLAMUSIC import app
import config


# ═══════════════════════════════════════
# OWNER CONFIG
# ═══════════════════════════════════════

OWNER_NAME = "SASUKE"
OWNER_USERNAME = "sasuke_qt"
OWNER_ID = 8672927645
OWNER_BIO = "𝐅ʀᴏᴍ 𝐒ᴜғғᴇʀɪɴɢ 𝐂ᴏᴍᴇs 𝐆ʟᴏʀʏ ⚡"


# ═══════════════════════════════════════
# PREMIUM EMOJI IDs
# ═══════════════════════════════════════

EMOJI_CROWN = "6269180384047533905"
EMOJI_STAR = "6269180384047533905"
EMOJI_ROSE = "6269180384047533905"


# ═══════════════════════════════════════
# /ROSE
# ═══════════════════════════════════════

@app.on_message(
    filters.command(
        ["rose"],
        prefixes=["/", "!", "."]
    )
)
async def rose_owner_info(client, message: Message):

    text = f"""
<b>🌹 OWNER DETAILS & PROFILE 🌹</b>

<b>👑 Name:</b>
<a href="tg://user?id={OWNER_ID}">{OWNER_NAME}</a>

<b>🆔 User ID:</b>
<code>{OWNER_ID}</code>

<b>💬 Username:</b>
@{OWNER_USERNAME}

<b>📝 Bio:</b>
<i>{OWNER_BIO}</i>

━━━━━━━━━━━━━━━━━━━━

<b>✨ Need Help or Support?</b>

Contact the owner using the buttons
below for bot setup, support & queries.
"""


    # ═══════════════════════════════════
    # COLOURED BUTTONS
    # ═══════════════════════════════════

    keyboard = {
        "inline_keyboard": [

            # 🔵 BLUE
            [
                {
                    "text": "ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ",
                    "url": f"https://t.me/{OWNER_USERNAME}",
                    "style": "primary",
                    "icon_custom_emoji_id": EMOJI_CROWN
                }
            ],

            # 🟢 GREEN
            [
                {
                    "text": "ᴍʏ ᴄʜᴀɴɴᴇʟ",
                    "url": "https://t.me/Aw_Music_channel",
                    "style": "success",
                    "icon_custom_emoji_id": EMOJI_STAR
                }
            ],

            # 🔴 RED
            [
                {
                    "text": "ʜᴇʟᴘ & sᴜᴘᴘᴏʀᴛ",
                    "url": f"https://t.me/{OWNER_USERNAME}",
                    "style": "danger",
                    "icon_custom_emoji_id": EMOJI_ROSE
                }
            ]
        ]
    }


    # ═══════════════════════════════════
    # TELEGRAM BOT API
    # ═══════════════════════════════════

    bot_token = getattr(config, "BOT_TOKEN", None)

    if not bot_token:
        return await message.reply_text(
            "❌ BOT_TOKEN not found in config.py"
        )

    api_url = (
        f"https://api.telegram.org/bot"
        f"{bot_token}/sendMessage"
    )


    data = {
        "chat_id": message.chat.id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_markup": keyboard,

        "reply_parameters": {
            "message_id": message.id
        }
    }


    try:

        async with httpx.AsyncClient(
            timeout=30
        ) as http:

            response = await http.post(
                api_url,
                json=data
            )

            result = response.json()

        if not result.get("ok"):

            error = result.get(
                "description",
                "Unknown Telegram API error"
            )

            await message.reply_text(
                f"❌ <b>Rose Button Error</b>\n\n"
                f"<code>{error}</code>",
                parse_mode="HTML"
            )

    except Exception as e:

        print(f"[ROSE ERROR] {e}")

        try:
            await message.reply_text(
                f"❌ <b>Rose Error</b>\n\n"
                f"<code>{str(e)[:500]}</code>",
                parse_mode="HTML"
            )
        except Exception:
            pass
