# ==========================================
# keyboards.py
# FF ID Management Bot Keyboards
# ==========================================

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ==========================================
# 🏠 HOME MENU
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
            )
        ],
        [
            InlineKeyboardButton(
                "🔍 Search UID",
                callback_data="search_uid"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Favorites",
                callback_data="favorites"
            )
        ],
        [
            InlineKeyboardButton(
                "♻️ Refresh",
                callback_data="refresh"
            )
        ]
    ])


# ==========================================
# 👑 ADMIN PANEL
# ==========================================

def admin_panel():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📥 Pending",
                callback_data="pending_list"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Stats",
                callback_data="stats"
            ),
            InlineKeyboardButton(
                "📜 Logs",
                callback_data="logs"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="broadcast"
            )
        ],
        [
            InlineKeyboardButton(
                "📤 Export",
                callback_data="export"
            )
        ]
    ])


# ==========================================
# ✅ APPROVE / REJECT
# ==========================================

def approval_buttons(uid):
    return InlineKeyboardMarkup([
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


# ==========================================
# 🗑 DELETE CONFIRMATION
# ==========================================

def delete_confirm(uid):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🗑 Confirm Delete",
                callback_data=f"delete:{uid}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="cancel"
            )
        ]
    ])


# ==========================================
# ✏️ EDIT BUTTON
# ==========================================

def edit_button(uid):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✏️ Edit",
                callback_data=f"edit:{uid}"
            )
        ]
    ])


# ==========================================
# ⭐ FAVORITE BUTTON
# ==========================================

def favorite_button(uid):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⭐ Add Favorite",
                callback_data=f"favorite:{uid}"
            )
        ]
    ])


# ==========================================
# 📤 EXPORT MENU
# ==========================================

def export_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📄 Export TXT",
                callback_data="export_txt"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Export CSV",
                callback_data="export_csv"
            )
        ]
    ])


# ==========================================
# 🗂 CATEGORY MENU
# ==========================================

def category_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 Heroic",
                callback_data="cat_Heroic"
            )
        ],
        [
            InlineKeyboardButton(
                "👑 Grandmaster",
                callback_data="cat_Grandmaster"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 Diamond",
                callback_data="cat_Diamond"
            )
        ],
        [
            InlineKeyboardButton(
                "🏆 Platinum",
                callback_data="cat_Platinum"
            )
        ]
    ])


# ==========================================
# 📋 SHOW IDS BUTTONS
# ==========================================

def ff_id_button(uid):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"🎮 UID: {uid}",
                callback_data=f"view:{uid}"
            )
        ]
    ])


# ==========================================
# 👀 VIEW DETAILS MENU
# ==========================================

def details_menu(uid):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👀 View",
                callback_data=f"view:{uid}"
            ),
            InlineKeyboardButton(
                "⭐ Favorite",
                callback_data=f"favorite:{uid}"
            )
        ],
        [
            InlineKeyboardButton(
                "✏️ Edit",
                callback_data=f"edit:{uid}"
            ),
            InlineKeyboardButton(
                "🗑 Delete",
                callback_data=f"delete_confirm:{uid}"
            )
        ]
    ])


# ==========================================
# 🏠 HOME + REFRESH
# ==========================================

def navigation_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            ),
            InlineKeyboardButton(
                "♻️ Refresh",
                callback_data="refresh"
            )
        ]
    ])


# ==========================================
# 🚫 NOT ALLOWED
# ==========================================

def not_allowed():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "❌ Not Allowed",
                callback_data="not_allowed"
            )
        ]
    ])
