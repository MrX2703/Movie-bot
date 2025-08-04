import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

VIDEO_FILE = "videos.json"

def load_data():
    if os.path.exists(VIDEO_FILE):
        with open(VIDEO_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(VIDEO_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.replace("/add", "").strip()
        name, stream, download = [x.strip() for x in text.split(",")]
        data = load_data()
        data[name] = {"stream": stream, "download": download}
        save_data(data)
        await update.message.reply_text(f"✅ Added movie: {name}")
    except Exception as e:
        await update.message.reply_text("❌ Usage: /add Movie Name , stream_link , download_link")

async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.replace("/get", "").strip()
    data = load_data()

    if name not in data:
        await update.message.reply_text("❌ Movie not found.")
        return

    movie = data[name]
    buttons = [
        [InlineKeyboardButton("▶️ Watch Online", url=movie["stream"])],
        [InlineKeyboardButton("⬇️ Download", url=movie["download"])]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"🎬 *{name}*", reply_markup=reply_markup, parse_mode="Markdown")

def main():
    TOKEN = os.getenv("8308772553:AAH7UczsM9zMttok86AKSWNMSz3Wt-bkXGo")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("add", add_movie))
    app.add_handler(CommandHandler("get", get_movie))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
