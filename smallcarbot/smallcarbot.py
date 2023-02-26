import os
import subprocess

import telegram
from telegram import ForceReply, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
#from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

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
        self.updater = Updater(TOKEN)
        self.application = self.updater.dispatcher
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("ping", self.ping))
        self.application.add_handler(CommandHandler("help", self.help_command))

        self.application.add_handler(MessageHandler(Filters.text & ~Filters.command, self.text_command))
        self.application.add_handler(MessageHandler(Filters.voice, self.voice_command))

        self.updater.start_polling()
        self.updater.idle()

    def start(self, update: Update, _: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text(
            'This bot provides interface for small car manipulating, use /help for more information.',
            reply_markup=ForceReply(selective=True),
            )
        photo = open(os.path.join(self.src_path, 'images', 'start_small_car.jpg'), 'rb')
        update.message.reply_photo(
            photo=photo,
            caption='Small car is Waveshare JetBot based on Jetson Nano.',
            reply_markup=ForceReply(selective=True)
            )

    def ping(self, update: Update, _: CallbackContext) -> None:
        """Send a message when the command /ping is issued."""
        update.message.reply_text(
            'Hello there, the bot is ready for work!',
            reply_markup=ForceReply(selective=True),
            )

    def help_command(self, update: Update, _: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text(
            'This command is in progress.',
            reply_markup=ForceReply(selective=True),
            )

    def text_command(self, update: Update, _: CallbackContext) -> None:
        """Receives text commands."""
        command = update.message.text
        command = command_processing.process_command(command)
        if command is None:
            update.message.reply_text(
                f'Не могу обработать команду {raw_command}',
                reply_markup=ForceReply(selective=True),
                )
        else:
            result = self.robot.execute(command)
            if result is None:
                update.message.reply_text(
                    f'Успешно выполнено!',
                    reply_markup=ForceReply(selective=True),
                    )
            else:
                photo = open(result, 'rb')
                update.message.reply_photo(
                    photo=photo,
                    reply_markup=ForceReply(selective=True)
                    )


    def voice_command(self, update: Update, _: CallbackContext) -> None:
        """Receives voice commands."""
        voice_info = context.bot.get_file(update.message.voice.file_id)
        voice = self.bot.getFile(voice_info)
        with open('smallcarbot/tmp/voice.ogg', 'wb') as voice_file:
            voice.download_to_memory(voice_file)

        subprocess.call(['ffmpeg', '-i', 'smallcarbot/tmp/voice.ogg', 'smallcarbot/tmp/voice.wav', '-y'])

        command = self.recodnize_audio()
        result = self.process_command(command)
        print(result)

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

    def process_command(self, raw_command, update: Update, _: CallbackContext):
        command = command_processing(command)
        if command is None:
            update.message.reply_text(
                f'Не могу обработать команду {raw_command}',
                reply_markup=ForceReply(selective=True),
                )
        else:
            result = self.robot.execute(command)
            if result is None:
                update.message.reply_text(
                    f'Успешно выполнено!',
                    reply_markup=ForceReply(selective=True),
                    )
            else:
                update.message.reply_photo(
                    photo=os.path.join(result),
                    reply_markup=ForceReply(selective=True)
                    )
