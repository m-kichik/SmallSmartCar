import os
import subprocess
import sqlite3

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

from .credentials import bot_token as TOKEN
from .utils import command_processing
from .database import DataBase

from smallcar.robot import SmallCar


class SmallCarBot:
    def __init__(self, on_board=False):
        self.bot = telegram.Bot(TOKEN)

        if on_board:
            self.robot = SmallCar()
        else:
            self.robot = None

        self.db_dir = os.path.abspath("database")
        self.db = DataBase(os.path.join(self.db_dir, "commands.db"))

        self.src_path = os.path.abspath("src")

        self.tmp_dir = os.path.abspath("tmp")
        self.raw_voice_file = os.path.join(self.tmp_dir, "voice.ogg")
        self.voice_file = os.path.join(self.tmp_dir, "voice.wav")

    def run(self):
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.db.create()

        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)

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

        try:
            command, command_name_rus = command_processing.process_command(raw_command)

            if command is None:
                await update.message.reply_text(
                    f"Can not compute command {raw_command}",
                    reply_markup=ForceReply(selective=True),
                )
            else:
                await self.process_command(command, command_name_rus, update)

            self.db.add_command(update.effective_user.id, raw_command)

        except Exception as e:
            self.db.add_command(update.effective_user.id, raw_command, type(e).__name__)

    async def voice_command(self, update: Update, context: CallbackContext) -> None:
        """Receives voice commands."""
        voice = await context.bot.get_file(update.message.voice.file_id)
        await voice.download_to_drive(self.raw_voice_file)

        subprocess.call(
            [
                "ffmpeg",
                "-i",
                self.raw_voice_file,
                self.voice_file,
                "-y",
            ]
        )

        command = self.recognize_audio()

        await update.message.reply_text(
            f'Computing command "{command.lower()}"',
            reply_markup=ForceReply(selective=True),
        )

        command, command_name_rus = command_processing.process_command(command)

        if command is None:
            await update.message.reply_text(
                f"Can not compute command {command}",
                reply_markup=ForceReply(selective=True),
            )
        else:
            await self.process_command(command, command_name_rus, update)

    async def process_command(self, command, command_name, update: Update) -> None:
        if self.robot is None:
            await update.message.reply_text(
                f"TEST: received command __{command_name}__.",
                reply_markup=ForceReply(selective=True),
            )
        else:
            result = self.robot.execute(command)
            print(result)
            if result["move_command"]:
                await update.message.reply_text(
                    "Well done!",
                    reply_markup=ForceReply(selective=True),
                )
            else:
                if result["image_path"] is not None:
                    photo = open(result["image_path"], "rb")
                    await update.message.reply_photo(
                        photo=photo, reply_markup=ForceReply(selective=True)
                    )
                else:
                    await update.message.reply_text(
                        result["status"],
                        reply_markup=ForceReply(selective=True),
                    )

    def recognize_audio(self):
        """Recognizes voice commands."""
        recognizer = speech_recognition.Recognizer()

        with speech_recognition.AudioFile(self.voice_file) as source:
            audio = recognizer.record(source)

        return recognizer.recognize_google(audio, language="ru-RU")
