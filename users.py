# ==========================================
# users.py
# FF ID Management Bot Users System
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import Message

import database as db
import keyboards

user_states = {}

# ==========================================
# START
# ==========================================

@Client.on_message(filters.command("start"))
async def start_cmd(client, message: Message):

    user = message.from_user

    db.add_user(
        user.id,
        user.first_name
    )

    await message.reply_text(
        "🎮 Welcome To FF ID Management Bot",
        reply_markup=keyboards.home_menu()
    )

# ==========================================
# TOTAL IDS
# ==========================================

@Client.on_message(filters.command("totalids"))
async def total_ids(client, message):

    total = db.total_ff_ids()

    await message.reply_text(
        f"📊 Total Saved IDs: {total}"
    )

# ==========================================
# TOTAL USERS
# ==========================================

@Client.on_message(filters.command("totalusers"))
async def total_users(client, message):

    total = db.total_users()

    await message.reply_text(
        f"👥 Total Users: {total}"
    )

# ==========================================
# SEARCH UID
# ==========================================

@Client.on_message(filters.command("search"))
async def search_uid(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/search UID"
        )

    uid = message.command[1]

    data = db.get_ff_by_uid(uid)

    if not data:
        return await message.reply_text(
            "❌ UID Not Found"
        )

    db.increase_view(uid)

    text = f"""
🎮 FF ID Details

🆔 UID: {data[2]}
👤 Nickname: {data[3]}
🏆 Category: {data[4]}
👁 Views: {data[6]}
⭐ Favorite: {data[7]}
📅 Saved: {data[8]}
"""

    await message.reply_text(text)

# ==========================================
# SEARCH NAME
# ==========================================

@Client.on_message(filters.command("searchname"))
async def search_name(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/searchname NAME"
        )

    name = " ".join(message.command[1:])

    results = db.search_nickname(name)

    if not results:
        return await message.reply_text(
            "❌ No Result Found"
        )

    text = "🔍 Results\n\n"

    for row in results:

        text += (
            f"🆔 {row[2]}\n"
            f"👤 {row[3]}\n"
            f"🏆 {row[4]}\n\n"
        )

    await message.reply_text(text)

# ==========================================
# SHOW IDS
# ==========================================

@Client.on_message(filters.command("showids"))
async def show_ids(client, message):

    data = db.get_all_ff_ids()

    if not data:
        return await message.reply_text(
            "❌ No IDs Saved"
        )

    text = "📋 Saved FF IDs\n\n"

    for row in data:

        text += (
            f"🆔 {row[2]}\n"
            f"👤 {row[3]}\n"
            f"🏆 {row[4]}\n\n"
        )

    await message.reply_text(text)

# ==========================================
# MOST VIEWED
# ==========================================

@Client.on_message(filters.command("top"))
async def top_viewed(client, message):

    data = db.most_viewed()

    if not data:
        return await message.reply_text(
            "❌ No Data"
        )

    await message.reply_text(
        f"🏆 Most Viewed UID\n\n"
        f"🆔 {data[0]}\n"
        f"👁 Views: {data[1]}"
    )
    # ==========================================
# ADD FAVORITE
# ==========================================

@Client.on_message(filters.command("fav"))
async def add_fav(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/fav UID"
        )

    uid = message.command[1]

    data = db.get_ff_by_uid(uid)

    if not data:
        return await message.reply_text(
            "❌ UID Not Found"
        )

    db.add_favorite(uid)

    await message.reply_text(
        f"⭐ Added To Favorites\n\nUID: {uid}"
    )


# ==========================================
# REMOVE FAVORITE
# ==========================================

@Client.on_message(filters.command("unfav"))
async def remove_fav(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/unfav UID"
        )

    uid = message.command[1]

    db.remove_favorite(uid)

    await message.reply_text(
        f"❌ Removed From Favorites\n\nUID: {uid}"
    )


# ==========================================
# FAVORITES LIST
# ==========================================

@Client.on_message(filters.command("favorites"))
async def favorite_list(client, message):

    data = db.get_favorites()

    if not data:
        return await message.reply_text(
            "📌 No Favorites Found"
        )

    text = "📌 Favorite FF IDs\n\n"

    for row in data:

        text += (
            f"🆔 {row[2]}\n"
            f"👤 {row[3]}\n"
            f"🏆 {row[4]}\n\n"
        )

    await message.reply_text(text)


# ==========================================
# CATEGORY FILTER
# ==========================================

async def show_category(message, category):

    data = db.get_by_category(category)

    if not data:
        return await message.reply_text(
            f"❌ No {category} IDs Found"
        )

    text = f"🏆 {category} IDs\n\n"

    for row in data[:50]:

        text += (
            f"🆔 {row[2]}\n"
            f"👤 {row[3]}\n\n"
        )

    await message.reply_text(text)


@Client.on_message(filters.command("bronze"))
async def bronze_cmd(client, message):
    await show_category(message, "Bronze")


@Client.on_message(filters.command("silver"))
async def silver_cmd(client, message):
    await show_category(message, "Silver")


@Client.on_message(filters.command("gold"))
async def gold_cmd(client, message):
    await show_category(message, "Gold")


@Client.on_message(filters.command("platinum"))
async def platinum_cmd(client, message):
    await show_category(message, "Platinum")


@Client.on_message(filters.command("diamond"))
async def diamond_cmd(client, message):
    await show_category(message, "Diamond")


@Client.on_message(filters.command("heroic"))
async def heroic_cmd(client, message):
    await show_category(message, "Heroic")


@Client.on_message(filters.command("grandmaster"))
async def grandmaster_cmd(client, message):
    await show_category(message, "Grandmaster")
    # ==========================================
# RECENT IDS
# ==========================================

@Client.on_message(filters.command("recent"))
async def recent_cmd(client, message):

    data = db.recent_ids()

    if not data:
        return await message.reply_text(
            "❌ No IDs Found"
        )

    text = "🆕 Recently Added FF IDs\n\n"

    for row in data:

        text += (
            f"🆔 {row[0]}\n"
            f"👤 {row[1]}\n"
            f"🏆 {row[2]}\n"
            f"📅 {row[3]}\n\n"
        )

    await message.reply_text(text)


# ==========================================
# TOP 10 VIEWED
# ==========================================

@Client.on_message(filters.command("top10"))
async def top10_viewed(client, message):

    data = db.top_10_viewed()

    if not data:
        return await message.reply_text(
            "❌ No Data Available"
        )

    text = "🏆 TOP 10 VIEWED FF IDs\n\n"

    for i, row in enumerate(data, start=1):

        text += (
            f"{i}. 🆔 {row[0]}\n"
            f"👤 {row[1]}\n"
            f"👁 Views: {row[2]}\n\n"
        )

    await message.reply_text(text)


# ==========================================
# START ADD ID
# ==========================================

@Client.on_message(filters.command("addid"))
async def addid_cmd(client, message):

    user_states[message.from_user.id] = {
        "step": "uid"
    }

    await message.reply_text(
        "🆔 Send FF UID"
    )


# ==========================================
# MULTI STEP FORM
# ==========================================

@Client.on_message(
    filters.text &
    ~filters.command([
        "start",
        "search",
        "showids",
        "recent",
        "top10"
    ])
)
async def add_form(client, message):

    user_id = message.from_user.id

    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state["step"] == "uid":

        state["uid"] = message.text.strip()
        state["step"] = "nickname"

        return await message.reply_text(
            "👤 Send Nickname"
        )

    elif state["step"] == "nickname":

        state["nickname"] = message.text.strip()
        state["step"] = "category"

        return await message.reply_text(
            "🏆 Send Category"
        )

    elif state["step"] == "category":

        uid = state["uid"]
        nickname = state["nickname"]
        category = message.text.strip()

        db.add_pending_request(
            user_id,
            uid,
            nickname,
            category
        )

        del user_states[user_id]

        await message.reply_text(
            f"📥 Request Submitted\n\n"
            f"UID: {uid}\n"
            f"Nickname: {nickname}\n"
            f"Category: {category}"
    )
