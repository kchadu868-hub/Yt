import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

TOKEN = '8394863520:AAGwM2eUFlIKGKQCO843GfQQ6fU5tn0OXHQ'

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (update.message and update.message.text):
        return
    url = update.message.text.strip()
    if 'youtube.com' in url or 'youtu.be' in url:
        msg = await update.message.reply_text("Downloading, please wait...")
        filename = "output.mp4"
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': filename,
            'noplaylist': True,
            'quiet': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open(filename, 'rb') as vid:
                await update.message.reply_video(vid)
            await msg.delete()
        except Exception as e:
            await update.message.reply_text(f"Download failed: {e}")
        finally:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, downloader))
    app.run_polling()