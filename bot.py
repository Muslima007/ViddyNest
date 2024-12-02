# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
# import yt_dlp
# import instaloader
# import os
# import logging
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info(f"Received /start command from {update.effective_user.username}")
#     await update.message.reply_text("Hello! Welcome to ViddyNest Telegram Bot!")
#
# # Help Command
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("Received /help command.")
#     await update.message.reply_text("I am a video downloader bot. Supported platforms:\n"
#                                     "- YouTube\n"
#                                     "- Instagram\n"
#                                     "Send me a valid link, and I'll download the video for you.")
#
# # Download YouTube Video
# async def download_youtube(url, chat_id, context):
#     try:
#         logger.info(f"Downloading YouTube video for chat_id: {chat_id} | URL: {url}")
#         ydl_opts = {
#             'format': 'best',
#             'outtmpl': f"{chat_id}_youtube.%(ext)s"
#         }
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#
#         # Find the downloaded file
#         for file in os.listdir():
#             if file.startswith(f"{chat_id}_youtube"):
#                 logger.info(f"Sending YouTube video file: {file} to chat_id: {chat_id}")
#                 await context.bot.send_video(chat_id=chat_id, video=open(file, 'rb'))
#                 os.remove(file)
#                 return
#
#     except Exception as e:
#         logger.error(f"Error downloading YouTube video for chat_id: {chat_id}: {e}")
#         await context.bot.send_message(chat_id, f"Error downloading YouTube video: {e}")
#
# # Download Instagram Content
# async def download_instagram(url, chat_id, context):
#     try:
#         logger.info(f"Downloading Instagram content for chat_id: {chat_id} | URL: {url}")
#         loader = instaloader.Instaloader()
#         shortcode = url.split("/")[-2]
#         post = instaloader.Post.from_shortcode(loader.context, shortcode)
#         loader.download_post(post, target=f"{chat_id}_instagram")
#
#         # Locate media
#         media_dir = f"{chat_id}_instagram"
#         for file in os.listdir(media_dir):
#             if file.endswith(".jpg") or file.endswith(".mp4"):
#                 file_path = os.path.join(media_dir, file)
#                 logger.info(f"Sending Instagram media file: {file} to chat_id: {chat_id}")
#                 if file.endswith(".jpg"):
#                     await context.bot.send_photo(chat_id=chat_id, photo=open(file_path, 'rb'))
#                 elif file.endswith(".mp4"):
#                     await context.bot.send_video(chat_id=chat_id, video=open(file_path, 'rb'))
#                 os.remove(file_path)
#
#     except Exception as e:
#         logger.error(f"Error downloading Instagram content for chat_id: {chat_id}: {e}")
#         await context.bot.send_message(chat_id, f"Error downloading Instagram content: {e}")
#
# # Handle Incoming Messages
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.message.chat_id
#     message = update.message.text.strip()
#
#     logger.info(f"Received message: {message} from chat_id: {chat_id}")
#
#     if "youtube.com" in message or "youtu.be" in message:
#         await context.bot.send_message(chat_id, "Downloading from YouTube...")
#         await download_youtube(message, chat_id, context)
#     elif "instagram.com" in message:
#         await context.bot.send_message(chat_id, "Downloading from Instagram...")
#         await download_instagram(message, chat_id, context)
#     else:
#         await context.bot.send_message(chat_id, "Unsupported URL or platform. Please send a valid YouTube or Instagram link.")
#
# # Main Function to Start the Bot
# def main():
#     TOKEN = "7558046028:AAHE-HQEIawWPKsKkL6uzExurPDvNyppp18"  # Replace with your bot token
#     application = Application.builder().token(TOKEN).build()
#
#     # Add Handlers
#     application.add_handler(CommandHandler("start", start_command))
#     application.add_handler(CommandHandler("help", help_command))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#
#     # Start Polling
#     logger.info("Starting the bot...")
#     application.run_polling()
#
# # Run the Bot
# if __name__ == "__main__":
#     main()
