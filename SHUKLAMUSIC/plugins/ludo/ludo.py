from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Temporary game rooms
ludo_games = {}


@Client.on_message(filters.command("ludo"))
async def ludo_start(client, message):
    keyboard = InlineKeyboardMarkup(
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
        "Create a game and invite your friends!\n\n"
        "👥 Players: 2–4\n"
        "🎯 Mode: Multiplayer\n\n"
        "Choose an option below:",
        reply_markup=keyboard,
    )


@Client.on_callback_query(filters.regex("^ludo_create$"))
async def ludo_create(client, callback_query):
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user

    if chat_id in ludo_games:
        await callback_query.answer(
            "A game already exists in this chat!",
            show_alert=True
        )
        return

    ludo_games[chat_id] = {
        "players": [user.id],
        "names": [user.first_name],
    }

    await callback_query.message.edit_text(
        "🎲 **LUDO ROOM CREATED**\n\n"
        f"👑 Host: {user.first_name}\n"
        "👥 Players: 1/4\n\n"
        "Ask your friends to press **JOIN GAME**.",
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

    await callback_query.answer("Game created! 🎲")


@Client.on_callback_query(filters.regex("^ludo_join$"))
async def ludo_join(client, callback_query):
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user

    if chat_id not in ludo_games:
        await callback_query.answer(
            "No Ludo game exists. Create one first!",
            show_alert=True
        )
        return

    game = ludo_games[chat_id]

    if user.id in game["players"]:
        await callback_query.answer(
            "You are already in the game!",
            show_alert=True
        )
        return

    if len(game["players"]) >= 4:
        await callback_query.answer(
            "Game is full! 👥",
            show_alert=True
        )
        return

    game["players"].append(user.id)
    game["names"].append(user.first_name)

    players_text = "\n".join(
        f"🎮 {i + 1}. {name}"
        for i, name in enumerate(game["names"])
    )

    await callback_query.message.edit_text(
        "🎲 **LUDO ROOM**\n\n"
        f"{players_text}\n\n"
        f"👥 Players: {len(game['players'])}/4",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 JOIN GAME",
                        callback_data="ludo_join"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🚀 START GAME",
                        callback_data="ludo_start"
                    )
                ],
            ]
        ),
    )

    await callback_query.answer("Joined the game! 🎲")


@Client.on_callback_query(filters.regex("^ludo_start$"))
async def ludo_game_start(client, callback_query):
    chat_id = callback_query.message.chat.id

    if chat_id not in ludo_games:
        await callback_query.answer(
            "No active game!",
            show_alert=True
        )
        return

    game = ludo_games[chat_id]

    if len(game["players"]) < 2:
        await callback_query.answer(
            "At least 2 players are required!",
            show_alert=True
        )
        return

    players_text = "\n".join(
        f"🎮 {i + 1}. {name}"
        for i, name in enumerate(game["names"])
    )

    await callback_query.message.edit_text(
        "🎲 **LUDO GAME READY!**\n\n"
        f"{players_text}\n\n"
        "🔥 Game engine connected!\n"
        "🎯 Next step: Dice + Ludo Board"
    )

    await callback_query.answer("Game started! 🎲")
