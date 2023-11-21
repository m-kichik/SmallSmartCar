import os
import subprocess

import telegram

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    filters,
)

import speech_recognition

from smallcarbot.credentials import bot_token as TOKEN
from smallcarbot.utils import command_processing

try:
    ON_BOARD = True
    from smallcar.robot import SmallCar

except ModuleNotFoundError:
    ON_BOARD = False


class SmallCarBot:
    def __init__(self):
        self.bot = telegram.Bot(TOKEN)
        if ON_BOARD:
            self.robot = SmallCar()
        else:
            self.robot = None
        self.src_path = os.path.abspath("smallcarbot/src")

    def run(self):
        self.application = Application.builder().token(TOKEN).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("ping", self.ping))
        self.application.add_handler(CommandHandler("help", self.help_command))

        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.text_command)
        )
        self.application.add_handler(MessageHandler(filters.VOICE, self.voice_command))

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start(self, update: Update, _: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        responce = "This bot provides interface for small car manipulating, use /help for more information."
        await update.message.reply_text(
            responce,
            reply_markup=ForceReply(selective=True),
        )
        photo = open(os.path.join(self.src_path, "images", "start_small_car.jpg"), "rb")
        await update.message.reply_photo(
            photo=photo,
            caption="Small car is Waveshare JetBot based on Jetson Nano.",
            reply_markup=ForceReply(selective=True),
        )
        if self.robot is None:
            await update.message.reply_text(
                "Bot works in TEST mode (no JetBot connection).",
                reply_markup=ForceReply(selective=True),
                )

    async def ping(self, update: Update, _: CallbackContext) -> None:
        """Send a message when the command /ping is issued."""
        responce = "Hello there, the bot is ready for work!"
        if self.robot is None:
            responce += " But only in TEST mode."
        await update.message.reply_text(
            responce,
            reply_markup=ForceReply(selective=True),
        )

    async def help_command(self, update: Update, _: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text(
            "This command is in progress.",
            reply_markup=ForceReply(selective=True),
        )

    async def text_command(self, update: Update, _: CallbackContext) -> None:
        """Receives text commands."""
        raw_command = update.message.text
        command, command_name_rus = command_processing.process_command(raw_command)

        if command is None:
            await update.message.reply_text(
                f"Не могу обработать команду {raw_command}",
                reply_markup=ForceReply(selective=True),
            )
        else:
            await self.process_command(command, command_name_rus, update)

    async def voice_command(self, update: Update, context: CallbackContext) -> None:
        """Receives voice commands."""
        voice = await context.bot.get_file(update.message.voice.file_id)
        voice_file = "smallcarbot/tmp/voice.ogg"
        await voice.download_to_drive(voice_file)

        subprocess.call(
            [
                "ffmpeg",
                "-i",
                "smallcarbot/tmp/voice.ogg",
                "smallcarbot/tmp/voice.wav",
                "-y",
            ]
        )

        command = self.recognize_audio()

        await update.message.reply_text(
            f'Выполняю команду "{command.lower()}"',
            reply_markup=ForceReply(selective=True),
        )

        command, command_name_rus = command_processing.process_command(command)

        if command is None:
            await update.message.reply_text(
                f"Не могу обработать команду {command}",
                reply_markup=ForceReply(selective=True),
            )
        else:
            await self.process_command(command, command_name_rus, update)

    async def process_command(self, command, command_name, update: Update) -> None:
        if self.robot is None:
            await update.message.reply_text(
                f"TEST: получена команда __{command_name}__.",
                reply_markup=ForceReply(selective=True),
            )
        else:
            result = self.robot.execute(command)
            if result is None:
                await update.message.reply_text(
                    "Успешно выполнено!",
                    reply_markup=ForceReply(selective=True),
                )
            else:
                photo = open(result, "rb")
                await update.message.reply_photo(
                    photo=photo, reply_markup=ForceReply(selective=True)
                )

    def recognize_audio(self):
        """Recognizes voice commands."""
        recognizer = speech_recognition.Recognizer()

        with speech_recognition.AudioFile("smallcarbot/tmp/voice.wav") as source:
            audio = recognizer.record(source)

        return recognizer.recognize_google(audio, language="ru-RU")
