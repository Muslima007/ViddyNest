from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import instaloader
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start command.")
    await update.message.reply_text('Hello! Welcome to ViddyNest telegram bot!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a video downloader bot. Send YouTube or Instagram links to download.')

# Function to download YouTube videos
async def download_youtube(url, chat_id, context):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f"{chat_id}_youtube.%(ext)s"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir():
            if file.startswith(f"{chat_id}_youtube"):
                await context.bot.send_video(chat_id=chat_id, video=open(file, 'rb'))
                os.remove(file)
                return
    except Exception as e:
        await context.bot.send_message(chat_id, f"Error downloading YouTube video: {e}")

# Function to download Instagram content
async def download_instagram(url, chat_id, context):
    try:
        loader = instaloader.Instaloader()
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=f"{chat_id}_instagram")
        # Locate media
        for file in os.listdir(f"{chat_id}_instagram"):
            if file.endswith(".jpg") or file.endswith(".mp4"):
                await context.bot.send_photo(chat_id=chat_id, photo=open(file, 'rb'))
                os.remove(file)
    except Exception as e:
        await context.bot.send_message(chat_id, f"Error downloading Instagram content: {e}")

# Function to handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    message = update.message.text

    if "youtube.com" in message or "youtu.be" in message:
        await context.bot.send_message(chat_id, "Downloading from YouTube...")
        await download_youtube(message, chat_id, context)
    elif "instagram.com" in message:
        await context.bot.send_message(chat_id, "Downloading from Instagram...")
        await download_instagram(message, chat_id, context)
    else:
        await context.bot.send_message(chat_id, "Unsupported URL or platform.")

# Start the bot
def main():
    TOKEN = os.getenv("7558046028:AAHE-HQEIawWPKsKkL6uzExurPDvNyppp18")
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()

