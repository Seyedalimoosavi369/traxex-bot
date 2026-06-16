from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")
URL = "https://seyedalimoosavi369.github.io/traxex_miniapp/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Open TRAXEX",
                web_app=WebAppInfo(url=URL)
            )
        ]
    ]

    await update.message.reply_text(
        "⚡ TRAXEX PRO SYSTEM",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("BOT RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()

