import os
import subprocess

import telegram
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from smallcarbot.credentials import bot_token as TOKEN
from smallcar.robot import SmallCar
from smallcarbot.utils import command_processing
import speech_recognition


class SmallCarBot():
    def __init__(self):
        self.bot = telegram.Bot(TOKEN)
        self.robot = SmallCar()
        self.src_path = os.path.abspath('smallcarbot/src')

    def run(self):
        self.application = Application.builder().token(TOKEN).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("ping", self.ping))
        self.application.add_handler(CommandHandler("help", self.help_command))

        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_text_command))
        self.application.add_handler(MessageHandler(filters.VOICE, self.get_voice_command))

        self.application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        await update.message.reply_text(
            'This bot provides interface for small car manipulating, use /help for more information.',
            reply_markup=ForceReply(selective=True),
            )
        await update.message.reply_photo(
            photo= os.path.join(self.src_path, 'images', 'start_small_car.jpg'),
            caption='Small car is Waveshare JetBot based on Jetson Nano.',
            reply_markup=ForceReply(selective=True)
            )

    async def ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /ping is issued."""
        await update.message.reply_text(
            'Hello there, the bot is ready for work!',
            reply_markup=ForceReply(selective=True),
            )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text(
            'This command is in progress.',
            reply_markup=ForceReply(selective=True),
            )

    async def get_text_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Receives text commands."""
        command = await update.message.reply_text(update.message.text)


    async def get_voice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Receives voice commands."""
        voice_info = await context.bot.get_file(update.message.voice.file_id)
        voice = await self.bot.getFile(voice_info)
        with open('smallcarbot/tmp/voice.ogg', 'wb') as voice_file:
            await voice.download_to_memory(voice_file)

        subprocess.call(['ffmpeg', '-i', 'smallcarbot/tmp/voice.ogg', 'smallcarbot/tmp/voice.wav', '-y'])

        command = await self.recodnize_audio()

        # await update.message.reply_text(
        #     command,
        #     reply_markup=ForceReply(selective=True),
        # )

    def recognize_audio(self):
        """Recognizes voice commands."""
        recognizer = speech_recognition.Recognizer()

        with speech_recognition.AudioFile('/home/rito4ka/dev/SmallSmartCar/smallcarbot/tmp/voice.wav') as source:
            audio = recognizer.record(source)

        return recognizer.recognize_google(audio, language="ru-RU")

    async def process_command(self, raw_command, update: Update, context: ContextTypes.DEFAULT_TYPE):
        command = await command_processing(command)
        if command is None:
            await update.message.reply_text(
                f'Не могу обработать команду {raw_command}',
                reply_markup=ForceReply(selective=True),
                )
        else:
            result = self.robot.execute(command)
            if result is None:
                await update.message.reply_text(
                    f'Успешно выполнено!',
                    reply_markup=ForceReply(selective=True),
                    )
            else:
                await update.message.reply_photo(
                    photo= os.path.join(result),
                    reply_markup=ForceReply(selective=True)
                    )