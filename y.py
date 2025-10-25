import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

# Replace this with your bot token from @BotFather
TOKEN = '8394863520:AAGwM2eUFlIKGKQCO843GfQQ6fU5tn0OXHQ'

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only process text messages
    if not (update.message and update.message.text):
        return
    url = update.message.text.strip()
    # Check for youtube url
    if 'youtube.com' in url or 'youtu.be' in url:
        msg = await update.message.reply_text("Downloading, please wait...")
        filename = "output.mp4"
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': filename,
            'noplaylist': True,
            'quiet': True,
            'cookiefile': 'cookies.txt'  # uses your browser cookies
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open(filename, 'rb') as vid:
                # Telegram bots can send files up to 50MB
                await update.message.reply_video(vid)
            await msg.delete()
        except Exception as e:
            await update.message.reply_text(f"Download failed: {e}")
        finally:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    # Only handle normal text messages (not commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, downloader))
    app.run_polling()
