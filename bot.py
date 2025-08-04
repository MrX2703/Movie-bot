from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

DATA_FILE = "videos.json"

# /add command handler
async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /add <movie_name> <watch_link> <download_link>")
        return

    movie_name = context.args[0].lower()
    watch_link = context.args[1]
    download_link = context.args[2]

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[movie_name] = {
        "watch": watch_link,
        "download": download_link
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    await update.message.reply_text(f"✅ Movie '{movie_name}' added successfully!")

# /get command handler
async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /get <movie_name>")
        return

    movie_name = context.args[0].lower()

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    if movie_name in data:
        movie = data[movie_name]
        reply = f"🎬 *{movie_name.title()}*\n\n▶️ [Watch Online]({movie['watch']})\n📥 [Download]({movie['download']})"
        await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        await update.message.reply_text(f"❌ Movie '{movie_name}' not found!")

# Bot start point
def main():
    import os
    TOKEN = os.environ["BOT_TOKEN"]

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("add", add_movie))
    app.add_handler(CommandHandler("get", get_movie))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
