from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from SHUKLAMUSIC import app


@app.on_message(filters.command("ludo"))
async def ludo_command(client, message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎲 CREATE GAME",
                    callback_data="ludo_create"
                )
            ],
            [
                InlineKeyboardButton(
                    "👥 JOIN GAME",
                    callback_data="ludo_join"
                )
            ],
        ]
    )

    await message.reply_text(
        "🎲 **LUDO GAME**\n\n"
        "Play Ludo with your friends on Telegram!\n\n"
        "👥 Players: 2–4\n"
        "🎯 Multiplayer Mode\n\n"
        "Choose an option below:",
        reply_markup=buttons,
    )


@app.on_callback_query(filters.regex("^ludo_create$"))
async def ludo_create(client, query):

    await query.answer(
        "🎲 Ludo room created!",
        show_alert=True
    )

    await query.message.edit_text(
        "🎲 **LUDO ROOM**\n\n"
        f"👑 Host: {query.from_user.mention}\n\n"
        "👥 Players: 1/4\n\n"
        "Waiting for players...",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 JOIN GAME",
                        callback_data="ludo_join"
                    )
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("^ludo_join$"))
async def ludo_join(client, query):

    await query.answer(
        "✅ You joined the Ludo game!",
        show_alert=True
    )
