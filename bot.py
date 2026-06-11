# ==========================================
# bot.py
# FF ID Management Bot (Main File)
# ==========================================

from pyrogram import Client
import config

# Import handlers
import admin
import users
import pending
import keyboards
import stats
import logs

# ==========================================
# BOT START
# ==========================================

app = Client(
    "ff_id_bot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

# ==========================================
# STARTUP MESSAGE
# ==========================================

@app.on_message()
def auto_save_users(client, message):
    try:
        import database as db

        if message.from_user:
            db.add_user(
                message.from_user.id,
                message.from_user.first_name
            )
    except:
        pass


# ==========================================
# RUN BOT
# ==========================================

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 FF ID Management Bot Started")
    print("=" * 50)

    app.run()
