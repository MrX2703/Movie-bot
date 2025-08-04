import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from link_cleaner import clean_links

TOKEN = os.getenv("8308772553:AAHPteT2VFqpQWCMHGucoC_h1stwGCNPeQo")

VIDEO_FILE = "videos.json"

def load_data():
    if not os.path.exists(VIDEO_FILE):
        return {}
    with open(VIDEO_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(VIDEO_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send /request <video_name> to get your video.")

async def add_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /add <video_name> <raw_url>")
        return

    name = context.args[0]
    raw_url = context.args[1]
    
    await update.message.reply_text(f"⏳ Cleaning link for {name}...")
    streaming, download = await clean_links(raw_url)

    if not streaming:
        await update.message.reply_text("❌ Failed to extract clean link.")
        return

    data = load_data()
    data[name.lower()] = {"stream": streaming, "download": download}
    save_data(data)
    
    await update.message.reply_text(f"✅ Video '{name}' added successfully.")

async def request_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /request <video_name>")
        return

    name = context.args[0].lower()
    data = load_data()
    if name not in data:
        await update.message.reply_text("⚠️ Video not found.")
        return
    
    vid = data[name]
    await update.message.reply_text(
        f"🎬 **{name.title()}**\n\n"
        f"▶️ [Stream Here]({vid['stream']})\n"
        f"⬇️ [Download Here]({vid['download']})",
        parse_mode="Markdown"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_video))
app.add_handler(CommandHandler("request", request_video))

if __name__ == "__main__":
    app.run_polling()
