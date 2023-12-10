import os
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import ForceReply

from smallcarbot.smallcarbot import SmallCarBot


class TestSmallCarBot(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bot = SmallCarBot(on_board=False)

    def test_creation(self):
        self.assertIsInstance(self.bot.db_dir, str)
        self.assertIsInstance(self.bot.src_path, str)
        self.assertIsInstance(self.bot.tmp_dir, str)
        self.assertIsInstance(self.bot.raw_voice_file, str)
        self.assertIsInstance(self.bot.voice_file, str)

    @patch("telegram.ext.CallbackContext")
    @patch("telegram.Update")
    @patch("builtins.open")
    async def test_start(self, mock_open, mock_update, mock_context):
        mock_open.return_value = "test_image"

        mock_update.message.reply_text = AsyncMock()
        mock_update.message.reply_photo = AsyncMock()

        await self.bot.start(mock_update, mock_context)

        mock_update.message.reply_text.assert_any_call(
            "This bot provides interface for small car manipulating, use /help for more information.",
            reply_markup=ForceReply(selective=True),
        )
        mock_update.message.reply_text.assert_any_call(
            "Bot works in TEST mode (no JetBot connection).",
            reply_markup=ForceReply(selective=True),
        )
        mock_update.message.reply_photo.assert_called_once()

    @patch("telegram.ext.CallbackContext")
    @patch("telegram.Update")
    async def test_ping(self, mock_update, mock_context):
        mock_update.message.reply_text = AsyncMock()

        await self.bot.ping(mock_update, mock_context)

        mock_update.message.reply_text.assert_any_call(
            "Hello there, the bot is ready for work! But only in TEST mode.",
            reply_markup=ForceReply(selective=True),
        )

    @patch("telegram.ext.CallbackContext")
    @patch("telegram.Update")
    async def test_help_command(self, mock_update, mock_context):
        mock_update.message.reply_text = AsyncMock()

        await self.bot.help_command(mock_update, mock_context)

        mock_update.message.reply_text.assert_any_call(
            "This command is in progress.",
            reply_markup=ForceReply(selective=True),
        )

    @patch("telegram.Update")
    async def test_process_command(self, mock_update):
        mock_update.message.reply_text = AsyncMock()

        await self.bot.process_command("test_command", "Test Command", mock_update)

        mock_update.message.reply_text.assert_called_once_with(
            "TEST: received command __Test Command__.",
            reply_markup=ForceReply(selective=True),
        )

    @patch("telegram.ext.CallbackContext")
    @patch("telegram.Update")
    async def test_text_command(self, mock_update, mock_context):
        mock_update.message.reply_text = AsyncMock()

        self.bot.process_command = AsyncMock()
        self.bot.db.add_command = MagicMock()

        with self.subTest("Normal command"):
            mock_update.message.text = "Поверни направо"
            await self.bot.text_command(mock_update, mock_context)

            self.bot.db.add_command.assert_called_once()
            self.bot.process_command.assert_called_once()

        with self.subTest("Bad command"):
            mock_update.message.text = "42"
            await self.bot.text_command(mock_update, mock_context)
            mock_update.message.reply_text.assert_any_call(
                "Can not compute command 42",
                reply_markup=ForceReply(selective=True),
            )


if __name__ == "__main__":
    unittest.main()
