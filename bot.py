import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ Replace with your actual token from BotFather
TOKEN = "8308772553:AAH7UczsM9zMttok86AKSWNMSz3Wt-bkXGo"

# Optional: Enable logging to see output in Render logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your bot.")

# Main function
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Add /start command handler
    app.add_handler(CommandHandler("start", start))

    # Start the bot
    print("Bot started...")
    await app.run_polling()

# Run the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
