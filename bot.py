import logging
import sqlite3
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TOKEN", "8625621495:AAFGXWA1iJTpfpQWdTchzGpF6TBPhw7k2D8")
MINIAPP_URL = "https://seyedalimoosavi369.github.io/traxex_miniapp/"
DB_NAME = os.path.expanduser("~/traxex/traxex.db")

CHANNELS = [
    "@chat_groupbot1",
    "@chat_chanelbot1"
]

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def save_user(telegram_id, username):
    try:
        conn = get_db()
        conn.execute('INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)', (telegram_id, username))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"DB error: {e}")

async def check_membership(bot, user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            pass
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username or user.first_name)

    is_member = await check_membership(context.bot, user.id)
    if not is_member:
        channel_list = "\n".join([f"👉 {ch}" for ch in CHANNELS])
        keyboard = [[InlineKeyboardButton("✅ I Joined", callback_data="check_membership")]]
        await update.message.reply_text(
            f"❌ Join these channels first:\n\n{channel_list}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    ref_url = f"{MINIAPP_URL}?ref={user.id}"
    keyboard = [[InlineKeyboardButton("⚡ Play Zeus", web_app=WebAppInfo(url=ref_url))]]
    await update.message.reply_text("⚡ Zeus", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    is_member = await check_membership(context.bot, user.id)
    if not is_member:
        channel_list = "\n".join([f"👉 {ch}" for ch in CHANNELS])
        keyboard = [[InlineKeyboardButton("✅ I Joined", callback_data="check_membership")]]
        await query.message.reply_text(
            f"❌ Join these channels first:\n\n{channel_list}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        ref_url = f"{MINIAPP_URL}?ref={user.id}"
        keyboard = [[InlineKeyboardButton("⚡ Play Zeus", web_app=WebAppInfo(url=ref_url))]]
        await query.message.reply_text("⚡ Zeus", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("Zeus Bot Running...")
    application.run_polling()

if __name__ == '__main__':
    main()
