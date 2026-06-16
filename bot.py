from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "توکن_رباتت"
URL = "https://seyedalimoosavi369.github.io/traxex_miniapp/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Open TRAXEX", url=URL)]
    ]

    await update.message.reply_text(
        "⚡ TRAXEX PRO ONLINE",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("BOT RUNNING...")
app.run_polling()
