# ==========================================
# users.py
# FF ID Management Bot User System
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import database as db
import config


# ==========================================
# START
# ==========================================

@Client.on_message(filters.command("start"))
def start(client, message):

    db.add_user(
        message.from_user.id,
        message.from_user.first_name
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add FF ID",
                callback_data="add_ff"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 Show IDs",
                callback_data="show_ids"
            )
        ],
        [
            InlineKeyboardButton(
                "🔍 Search UID",
                callback_data="search_uid"
            )
        ]
    ])

    message.reply(
        "🎮 Welcome To FF ID Management Bot",
        reply_markup=buttons
    )


# ==========================================
# SHOW IDS
# ==========================================

@Client.on_callback_query(
    filters.regex("^show_ids$")
)
def show_ids(client, callback_query):

    ids = db.get_all_ff_ids()

    if not ids:
        return callback_query.message.reply(
            "📭 No FF IDs Found"
        )

    for item in ids:

        uid = item[2]

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"🎮 {uid}",
                    callback_data=f"view:{uid}"
                )
            ]
        ])

        callback_query.message.reply(
            f"🆔 UID: {uid}",
            reply_markup=buttons
        )


# ==========================================
# VIEW DETAILS
# ==========================================

@Client.on_callback_query(
    filters.regex(r"^view:")
)
def view_details(client, callback_query):

    uid = callback_query.data.split(":")[1]

    data = db.get_ff_by_uid(uid)

    if not data:
        return callback_query.answer(
            "UID Not Found",
            show_alert=True
        )

    db.increase_view(uid)

    text = (
        f"🎮 FF ID Details\n\n"
        f"🆔 UID: {data[2]}\n"
        f"👤 Nickname: {data[3]}\n"
        f"🏆 Category: {data[4]}\n"
        f"📊 Status: {data[5]}\n"
        f"👀 Views: {data[6]}\n"
        f"📅 Saved: {data[8]}"
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⭐ Favorite",
                callback_data=f"favorite:{uid}"
            )
        ]
    ])

    callback_query.message.reply(
        text,
        reply_markup=buttons
    )


# ==========================================
# ADD FAVORITE
# ==========================================

@Client.on_callback_query(
    filters.regex(r"^favorite:")
)
def add_favorite(client, callback_query):

    uid = callback_query.data.split(":")[1]

    db.add_favorite(uid)

    callback_query.answer(
        "⭐ Added To Favorites"
    )


# ==========================================
# SEARCH UID
# ==========================================

@Client.on_message(filters.command("search"))
def search_uid(client, message):

    args = message.text.split()

    if len(args) < 2:
        return message.reply(
            "Usage:\n/search UID"
        )

    uid = args[1]

    data = db.get_ff_by_uid(uid)

    if not data:
        return message.reply(
            "❌ UID Not Found"
        )

    db.increase_view(uid)

    message.reply(
        f"🎮 Result Found\n\n"
        f"🆔 UID: {data[2]}\n"
        f"👤 Nickname: {data[3]}\n"
        f"🏆 Category: {data[4]}"
    )


# ==========================================
# ADD FF ID
# ==========================================

@Client.on_message(filters.command("add"))
def add_ff(client, message):

    args = message.text.split(maxsplit=3)

    if len(args) < 4:
        return message.reply(
            "Usage:\n/add UID NAME CATEGORY"
        )

    uid = args[1]
    nickname = args[2]
    category = args[3]

    if not config.ALLOW_DUPLICATE_UID:
        if db.uid_exists(uid):
            return message.reply(
                "❌ UID Already Exists"
            )

    db.add_pending(
        message.from_user.id,
        uid,
        nickname,
        category
    )

    for admin in config.ADMIN_IDS:
        try:
            client.send_message(
                admin,
                f"📥 New FF ID Request\n\n"
                f"UID: {uid}\n"
                f"Name: {nickname}\n"
                f"Category: {category}"
            )
        except:
            pass

    message.reply(
        "✅ Submitted For Approval"
    )


# ==========================================
# MY IDS
# ==========================================

@Client.on_message(filters.command("myids"))
def my_ids(client, message):

    ids = db.get_all_ff_ids()

    found = False

    for item in ids:

        if item[1] == message.from_user.id:

            found = True

            message.reply(
                f"🆔 {item[2]}\n"
                f"👤 {item[3]}"
            )

    if not found:
        message.reply(
            "📭 No FF IDs Found"
        )


# ==========================================
# HOME BUTTON
# ==========================================

@Client.on_callback_query(
    filters.regex("^home$")
)
def home(client, callback_query):

    callback_query.message.reply(
        "🏠 Home Menu\n\n"
        "/add\n"
        "/search\n"
        "/myids"
    )


# ==========================================
# REFRESH
# ==========================================

@Client.on_callback_query(
    filters.regex("^refresh$")
)
def refresh(client, callback_query):

    callback_query.answer(
        "♻️ Refreshed"
  )
