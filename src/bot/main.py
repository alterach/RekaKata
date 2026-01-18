"""Telegram Bot for RekaKata."""
import asyncio
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from src.core.prompt_engine import PromptEngine
from config.logging_config import log
from config.settings import get_settings


class TelegramBot:
    """Telegram bot interface for RekaKata."""

    def __init__(self):
        """Initialize Telegram bot."""
        self.settings = get_settings()
        self.engine = PromptEngine()
        self.application = Application.builder().token(
            self.settings.telegram_bot_token
        ).build()

        # Register handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("generate", self.generate_command))
        self.application.add_handler(CommandHandler("debug", self.debug_command))
        self.application.add_handler(CommandHandler("export", self.export_command))
        self.application.add_handler(CommandHandler("ping", self.ping_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text)
        )

        log.info("TelegramBot initialized")

    async def ping_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /ping command."""
        await update.message.reply_text("🏓 Pong! Bot is alive and running.")

    async def start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /start command.

        Args:
            update: Telegram update
            context: Bot context
        """
        welcome_message = """
🎬 *RekaKata - UGC Prompt Generator*

Selamat datang! Saya akan membantu kamu membuat prompt text-to-video yang berkualitas tinggi.

*Perintah yang tersedia:*
• `/generate <ide>` - Buat prompt baru
• `/export` - Download prompt terakhir sebagai file .md
• `/help` - Lihat bantuan

*Contoh penggunaan:*
/generate Jualin skincare pagi hari yang bagus buat wajah berminyak

Atau ketik langsung ide kamu, dan saya akan bantu buatkan promptnya! ✨
"""

        await update.message.reply_text(welcome_message, parse_mode="Markdown")
        log.info(f"User {update.effective_user.id} started the bot")

    async def generate_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /generate command.

        Args:
            update: Telegram update
            context: Bot context
        """
        # Check if user provided input
        if not context.args:
            await update.message.reply_text(
                "⚠️ Mohon masukkan ide konten kamu!\n\nContoh: /generate Jualin skincare pagi hari",
                parse_mode="Markdown",
            )
            return

        user_input = " ".join(context.args)

        # Send processing message
        processing_msg = await update.message.reply_text("⏳ Sedang memproses...")

        try:
            # Generate prompt in background thread
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, self.engine.generate_prompt, user_input)

            if not result["success"]:
                await processing_msg.delete()
                await update.message.reply_text(
                    f"❌ *Error:* {result.get('error', 'Unknown error')}",
                    parse_mode="Markdown",
                )
                return

            # Delete processing message
            await processing_msg.delete()

            # Send result
            await self._send_prompt_result(update, result)

        except Exception as e:
            await processing_msg.delete()
            await update.message.reply_text(
                f"❌ *Terjadi kesalahan:* {str(e)}", parse_mode="Markdown"
            )
            log.error(f"Error in generate command: {e}", exc_info=True)

    async def handle_text(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle direct text messages (not commands).

        Args:
            update: Telegram update
            context: Bot context
        """
        user_input = update.message.text

        # Send processing message
        processing_msg = await update.message.reply_text("⏳ Sedang memproses...")

        try:
            # Generate prompt in background thread
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, self.engine.generate_prompt, user_input)

            if not result["success"]:
                await processing_msg.delete()
                await update.message.reply_text(
                    f"❌ *Error:* {result.get('error', 'Unknown error')}",
                    parse_mode="Markdown",
                )
                return

            # Delete processing message
            await processing_msg.delete()

            # Send result
            await self._send_prompt_result(update, result)

        except Exception as e:
            await processing_msg.delete()
            await update.message.reply_text(
                f"❌ *Terjadi kesalahan:* {str(e)}", parse_mode="Markdown"
            )
            log.error(f"Error in handle_text: {e}", exc_info=True)

    async def _send_prompt_result(
        self, update: Update, result: dict
    ) -> None:
        """
        Send formatted prompt result to user.

        Args:
            update: Telegram update
            result: Generated prompt result
        """
        telegram_output = result["telegram_output"]

        # Send main output
        await update.message.reply_text(
            telegram_output, parse_mode="Markdown", disable_web_page_preview=True
        )

        # Send file download hint
        await update.message.reply_text(
            "📁 Ketik `/export` untuk download file .md",
            parse_mode="Markdown",
        )

    async def export_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /export command.

        Args:
            update: Telegram update
            context: Bot context
        """
        processing_msg = await update.message.reply_text("⏳ Sedang menyiapkan file...")

        try:
            # Export last generated prompt
            filepath = self.engine.export_last_generated(format="md")

            if not filepath:
                await processing_msg.delete()
                await update.message.reply_text(
                    "⚠️ Tidak ada prompt yang tersedia untuk diekspor. "
                    "Buat prompt dulu dengan /generate",
                    parse_mode="Markdown",
                )
                return

            # Send file
            file_path = Path(filepath)
            await update.message.reply_document(
                document=open(file_path, "rb"),
                filename=file_path.name,
                caption=f"📄 {file_path.name}",
            )

            await processing_msg.delete()
            log.info(f"Exported file: {filepath}")

        except Exception as e:
            await processing_msg.delete()
            await update.message.reply_text(
                f"❌ *Gagal mengekspor:* {str(e)}", parse_mode="Markdown"
            )
            log.error(f"Error in export command: {e}", exc_info=True)

    async def debug_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /debug command to show raw API response.

        Args:
            update: Telegram update
            context: Bot context
        """
        if not context.args:
            await update.message.reply_text("⚠️ Masukkan ide untuk debug!", parse_mode="Markdown")
            return

        user_input = " ".join(context.args)
        processing_msg = await update.message.reply_text("🐞 DEBUG MODE: Memproses...")

        try:
            # Generate prompt in background thread
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, self.engine.generate_prompt, user_input)

            if not result["success"]:
                await processing_msg.delete()
                await update.message.reply_text(f"❌ Error: {result.get('error')}")
                return

            await processing_msg.delete()

            # Extract raw response
            structured = result.get("structured_result", {})
            raw_response = structured.get("raw_response", "No raw response found")

            # Send raw response as code block
            # Split if too long (Telegram limit 4096)
            if len(raw_response) > 4000:
                raw_response = raw_response[:4000] + "... (truncated)"

            await update.message.reply_text(
                f"🐞 **RAW AI RESPONSE**:\n\n```\n{raw_response}\n```",
                parse_mode="Markdown"
            )

        except Exception as e:
            await processing_msg.delete()
            await update.message.reply_text(f"❌ Exception: {str(e)}")
            log.error(f"Error in debug command: {e}", exc_info=True)

    async def help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /help command.

        Args:
            update: Telegram update
            context: Bot context
        """
        help_message = """
🎬 *RekaKata - Bantuan*

*Perintah:*

`/start` - Mulai bot dan lihat pesan selamat datang

`/generate <ide>` - Buat prompt baru
  Contoh: /generate Jualin skincare pagi hari

`/export` - Download prompt terakhir sebagai file .md

`/help` - Lihat pesan bantuan ini

*Tips:*
• Kamu juga bisa langsung mengetik ide tanpa perintah
• Semakin spesifik ide kamu, semakin bagus promptnya
• Gunakan bahasa Indonesia atau Inggris

*Platform yang didukung:*
• TikTok
• Instagram Reels
• YouTube Shorts

Butuh bantuan lainnya? Hubungi admin! 🆘
"""

        await update.message.reply_text(help_message, parse_mode="Markdown")

    def run(self):
        """Start the bot."""
        log.info("Starting Telegram bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point for the bot."""
    bot = TelegramBot()
    bot.run()


if __name__ == "__main__":
    main()
