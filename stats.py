# ==========================================
# stats.py
# FF ID Management Bot Statistics System
# ==========================================

from pyrogram import Client, filters
import config
import database as db


# ==========================================
# 👑 ADMIN CHECK
# ==========================================

def is_admin(user_id):
    return user_id in config.ADMIN_IDS


# ==========================================
# 📊 BOT STATS
# ==========================================

@Client.on_message(filters.command("stats"))
def stats_command(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    total_users = db.total_users()
    total_ids = db.total_ff_ids()

    try:
        top = db.most_viewed()

        if top:
            top_uid = top[0]
            top_views = top[1]
        else:
            top_uid = "None"
            top_views = 0

    except:
        top_uid = "None"
        top_views = 0

    pending_count = len(db.get_pending_requests())

    message.reply(
        f"📊 FF ID BOT STATS\n\n"
        f"👥 Total Users: {total_users}\n"
        f"🎮 Total FF IDs: {total_ids}\n"
        f"📥 Pending Requests: {pending_count}\n"
        f"📈 Most Viewed UID: {top_uid}\n"
        f"👀 Views: {top_views}"
    )


# ==========================================
# 👥 TOTAL USERS
# ==========================================

@Client.on_message(filters.command("users"))
def users_count(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    message.reply(
        f"👥 Total Users: {db.total_users()}"
    )


# ==========================================
# 🎮 TOTAL FF IDS
# ==========================================

@Client.on_message(filters.command("ffids"))
def ffids_count(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    message.reply(
        f"🎮 Total FF IDs: {db.total_ff_ids()}"
    )


# ==========================================
# 📈 MOST VIEWED UID
# ==========================================

@Client.on_message(filters.command("topuid"))
def top_uid(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    data = db.most_viewed()

    if not data:
        return message.reply(
            "📭 No Viewed UID Found"
        )

    message.reply(
        f"🏆 Most Viewed UID\n\n"
        f"🆔 UID: {data[0]}\n"
        f"👀 Views: {data[1]}"
    )


# ==========================================
# 📥 PENDING COUNT
# ==========================================

@Client.on_message(filters.command("pendingstats"))
def pending_stats(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    pending = len(db.get_pending_requests())

    message.reply(
        f"📥 Pending Requests: {pending}"
    )


# ==========================================
# ⭐ FAVORITE COUNT
# ==========================================

@Client.on_message(filters.command("favoritescount"))
def favorites_count(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    try:
        data = db.get_all_ff_ids()

        count = 0

        for row in data:
            if row[7] == 1:
                count += 1

        message.reply(
            f"⭐ Total Favorites: {count}"
        )

    except:
        message.reply(
            "⭐ Total Favorites: 0"
      )
