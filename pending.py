# ==========================================
# pending.py
# FF ID Management Bot Pending System
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import database as db
import config


# ==========================================
# 👑 ADMIN CHECK
# ==========================================

def is_admin(user_id):
    return user_id in config.ADMIN_IDS


# ==========================================
# 📥 SHOW PENDING REQUESTS
# ==========================================

@Client.on_message(filters.command("pending"))
def pending_list(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    requests = db.get_pending_requests()

    if not requests:
        return message.reply("📭 No Pending Requests")

    for req in requests:

        uid = req["uid"]
        user_id = req["user_id"]
        nickname = req["nickname"]
        category = req["category"]

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Approve",
                    callback_data=f"approve:{uid}"
                ),
                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject:{uid}"
                )
            ]
        ])

        message.reply(
            f"📥 Pending Request\n\n"
            f"🆔 UID: {uid}\n"
            f"🎮 Name: {nickname}\n"
            f"🏆 Category: {category}\n"
            f"👤 User ID: {user_id}",
            reply_markup=buttons
        )


# ==========================================
# ✅ APPROVE REQUEST
# ==========================================

@Client.on_callback_query(
    filters.regex(r"^approve:")
)
def approve_request(client, callback_query):

    if not is_admin(callback_query.from_user.id):
        return callback_query.answer(
            "❌ Not Allowed",
            show_alert=True
        )

    uid = callback_query.data.split(":")[1]

    data = db.approve_request(uid)

    if not data:
        return callback_query.answer(
            "Request not found",
            show_alert=True
        )

    user_id = data[1]

    # Add Log
    db.add_log(
        "approve",
        callback_query.from_user.id,
        uid
    )

    # Notify User
    try:
        client.send_message(
            user_id,
            f"🎉 Congratulations!\n\n"
            f"Your FF ID ({uid}) has been approved."
        )
    except:
        pass

    callback_query.message.edit_text(
        f"✅ Approved\n\nUID: {uid}"
    )


# ==========================================
# ❌ REJECT REQUEST
# ==========================================

@Client.on_callback_query(
    filters.regex(r"^reject:")
)
def reject_request(client, callback_query):

    if not is_admin(callback_query.from_user.id):
        return callback_query.answer(
            "❌ Not Allowed",
            show_alert=True
        )

    uid = callback_query.data.split(":")[1]

    requests = db.get_pending_requests()

    target_user = None

    for req in requests:
        if req["uid"] == uid:
            target_user = req["user_id"]
            break

    db.reject_request(uid)

    db.add_log(
        "reject",
        callback_query.from_user.id,
        uid
    )

    # Notify User
    if target_user:
        try:
            client.send_message(
                target_user,
                f"❌ Sorry!\n\n"
                f"Your FF ID ({uid}) was rejected."
            )
        except:
            pass

    callback_query.message.edit_text(
        f"❌ Rejected\n\nUID: {uid}"
    )


# ==========================================
# 📊 PENDING COUNT
# ==========================================

@Client.on_message(filters.command("pendingcount"))
def pending_count(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    requests = db.get_pending_requests()

    message.reply(
        f"📥 Total Pending Requests: {len(requests)}"
    )


# ==========================================
# 🗑 CLEAR ALL PENDING
# ==========================================

@Client.on_message(filters.command("clearpending"))
def clear_pending(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🗑 Confirm",
                callback_data="confirm_clear_pending"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="cancel_clear_pending"
            )
        ]
    ])

    message.reply(
        "⚠️ Clear all pending requests?",
        reply_markup=buttons
    )


# ==========================================
# ✅ CONFIRM CLEAR
# ==========================================

@Client.on_callback_query(
    filters.regex("^confirm_clear_pending$")
)
def confirm_clear_pending(client, callback_query):

    if not is_admin(callback_query.from_user.id):
        return callback_query.answer(
            "❌ Not Allowed",
            show_alert=True
        )

    try:
        db.clear_pending()
    except:
        pass

    callback_query.message.edit_text(
        "✅ All pending requests cleared."
    )


# ==========================================
# ❌ CANCEL CLEAR
# ==========================================

@Client.on_callback_query(
    filters.regex("^cancel_clear_pending$")
)
def cancel_clear_pending(client, callback_query):

    callback_query.message.edit_text(
        "❌ Cancelled."
      )
