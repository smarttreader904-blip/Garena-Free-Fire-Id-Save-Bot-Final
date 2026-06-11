# ==========================================
# bot.py
# FF ID Management Bot Main File
# ==========================================

from pyrogram import Client
import config

# Import Handlers
import users
import admin
import pending
import logs
import stats
import keyboards
import utils
import database


# ==========================================
# START BOT
# ==========================================

app = Client(
    "ff_id_bot",
    bot_token=config.BOT_TOKEN
)


# ==========================================
# BOT START MESSAGE
# ==========================================

@app.on_message()
async def auto_register(client, message):

    if message.from_user:

        database.add_user(
            message.from_user.id,
            message.from_user.first_name
        )


# ==========================================
# RUN BOT
# ==========================================

if __name__ == "__main__":

    print("=" * 40)
    print("✅ FF ID BOT STARTED")
    print("=" * 40)

    app.run()
