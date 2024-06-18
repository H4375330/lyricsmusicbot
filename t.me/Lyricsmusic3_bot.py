import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import youtube_dl
from pydub import AudioSegment

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('7494721071:AAHov6Z7ut4F7-5LU3xTPFfS3ByUZHZjsJk')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define commands
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I am a music bot. Use /play <YouTube URL> to play music.')

def play(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text('Please provide a YouTube URL.')
        return
    
    url = context.args[0]
    update.message.reply_text('Downloading...')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_song.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.startswith("downloaded_song") and file.endswith(".mp3"):
            audio = AudioSegment.from_file(file)
            audio.export("song.ogg", format="ogg")

    with open("song.ogg", "rb") as audio_file:
        update.message.reply_audio(audio=audio_file)

    os.remove("downloaded_song.mp3")
    os.remove("song.ogg")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('play', play))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
