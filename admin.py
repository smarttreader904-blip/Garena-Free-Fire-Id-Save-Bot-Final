from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import database as db
import config


# =========================
# 🔐 ADMIN CHECK
# =========================
def is_admin(user_id):
    return user_id in config.ADMIN_IDS


# =========================
# 📥 PENDING REQUEST LIST
# =========================
@Client.on_message(filters.command("pending") & filters.private)
def pending_requests(client, message):
    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    requests = db.get_pending_requests()

    if not requests:
        return message.reply("📭 No pending requests")

    for req in requests:
        uid = req["uid"]
        ffid = req["ff_id"]

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve:{uid}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{uid}")
            ]
        ])

        message.reply(
            f"📥 Pending FF ID Request\n\n"
            f"👤 UID: {uid}\n"
            f"🎮 FF ID: {ffid}",
            reply_markup=buttons
        )


# =========================
# ✅ APPROVE REQUEST
# =========================
@Client.on_callback_query(filters.regex(r"approve:(.+)"))
def approve_request(client, callback_query):
    if not is_admin(callback_query.from_user.id):
        return callback_query.answer("Not allowed", show_alert=True)

    uid = callback_query.data.split(":")[1]

    data = db.approve_request(uid)

    # user notify
    client.send_message(
        uid,
        "🎉 আপনার FF ID Approve করা হয়েছে!"
    )

    callback_query.message.edit_text("✅ Approved Successfully")


# =========================
# ❌ REJECT REQUEST
# =========================
@Client.on_callback_query(filters.regex(r"reject:(.+)"))
def reject_request(client, callback_query):
    if not is_admin(callback_query.from_user.id):
        return callback_query.answer("Not allowed", show_alert=True)

    uid = callback_query.data.split(":")[1]

    db.reject_request(uid)

    # user notify
    client.send_message(
        uid,
        "❌ দুঃখিত, আপনার FF ID Reject করা হয়েছে!"
    )

    callback_query.message.edit_text("❌ Rejected")


# =========================
# 🗑 DELETE FF ID
# =========================
@Client.on_callback_query(filters.regex(r"delete:(.+)"))
def delete_ffid(client, callback_query):
    if not is_admin(callback_query.from_user.id):
        return callback_query.answer("Not Allowed", show_alert=True)

    ff_id = callback_query.data.split(":")[1]

    db.delete_ff_id(ff_id)

    callback_query.message.edit_text("🗑 Deleted Successfully")


# =========================
# 📢 BROADCAST MESSAGE
# =========================
@Client.on_message(filters.command("broadcast") & filters.private)
def broadcast(client, message):
    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    text = message.text.replace("/broadcast", "").strip()

    users = db.get_all_users()

    count = 0
    for user in users:
        try:
            client.send_message(user, f"📢 Broadcast:\n\n{text}")
            count += 1
        except:
            pass

    message.reply(f"✅ Broadcast sent to {count} users")


# =========================
# 📊 STATS
# =========================
@Client.on_message(filters.command("stats") & filters.private)
def stats(client, message):
    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    total_users = db.total_users()
    total_ids = db.total_ff_ids()

    message.reply(
        f"📊 Bot Stats\n\n"
        f"👥 Users: {total_users}\n"
        f"🎮 FF IDs: {total_ids}"
  )
