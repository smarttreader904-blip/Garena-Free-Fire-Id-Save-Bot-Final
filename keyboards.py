# ==========================================
# keyboards.py
# FF ID Management Bot Keyboards
# ==========================================

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# ==========================================
# HOME MENU
# ==========================================

def home_menu():
    return InlineKeyboardMarkup([
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
            ),
            InlineKeyboardButton(
                "🔍 Search UID",
                callback_data="search_uid"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Favorites",
                callback_data="favorites"
            ),
            InlineKeyboardButton(
                "📊 Stats",
                callback_data="stats"
            )
        ],
        [
            InlineKeyboardButton(
                "📥 Pending",
                callback_data="pending"
            )
        ]
    ])


# ==========================================
# ADMIN PANEL
# ==========================================

def admin_panel():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📥 Pending Requests",
                callback_data="pending_list"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="broadcast"
            ),
            InlineKeyboardButton(
                "📊 Stats",
                callback_data="admin_stats"
            )
        ],
        [
            InlineKeyboardButton(
                "📜 Logs",
                callback_data="logs"
            ),
            InlineKeyboardButton(
                "📤 Export",
                callback_data="export"
            )
        ]
    ])


# ==========================================
# APPROVE / REJECT
# ==========================================

def approve_reject(uid):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve_{uid}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject_{uid}"
            )
        ]
    ])


# ==========================================
# DELETE CONFIRM
# ==========================================

def delete_confirm(uid):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🗑 Confirm Delete",
                callback_data=f"delete_{uid}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="cancel_delete"
            )
        ]
    ])


# ==========================================
# FF ID ACTIONS
# ==========================================

def ff_actions(uid):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⭐ Favorite",
                callback_data=f"fav_{uid}"
            ),
            InlineKeyboardButton(
                "❌ Unfavorite",
                callback_data=f"unfav_{uid}"
            )
        ],
        [
            InlineKeyboardButton(
                "✏️ Edit",
                callback_data=f"edit_{uid}"
            ),
            InlineKeyboardButton(
                "🗑 Delete",
                callback_data=f"delete_{uid}"
            )
        ]
    ])


# ==========================================
# REFRESH BUTTON
# ==========================================

def refresh_button():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "♻️ Refresh",
                callback_data="refresh"
            )
        ]
    ])


# ==========================================
# BACK HOME
# ==========================================

def back_home():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            )
        ]
    ])


# ==========================================
# EXPORT MENU
# ==========================================

def export_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📄 Export TXT",
                callback_data="export_txt"
            ),
            InlineKeyboardButton(
                "📊 Export CSV",
                callback_data="export_csv"
            )
        ]
    ])


# ==========================================
# CATEGORY MENU
# ==========================================

def category_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 Heroic",
                callback_data="cat_heroic"
            ),
            InlineKeyboardButton(
                "👑 Grandmaster",
                callback_data="cat_grandmaster"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 Diamond",
                callback_data="cat_diamond"
            ),
            InlineKeyboardButton(
                "🥈 Platinum",
                callback_data="cat_platinum"
            )
        ]
    ])
