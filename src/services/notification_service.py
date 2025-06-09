import logging
from typing import Set
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from ..config.config_manager import ConfigManager
import asyncio

class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = ConfigManager().config
        self.admin_ids: Set[int] = self.config.bot.admin_ids

    async def safe_send_message(self, chat_id: int, text: str) -> None:
        """Safe message sending with error handling"""
        try:
            await self.bot.get_chat(chat_id)
            await self.bot.send_message(chat_id, text)
        except TelegramBadRequest as e:
            if "chat not found" in str(e):
                logging.warning(f"Chat {chat_id} not available")
            else:
                logging.error(f"Send error: {e}")
        except Exception as e:
            logging.error(f"Critical error: {e}")

    async def send_notification(self, event: str, **kwargs) -> None:
        """Send notification to all administrators"""
        if not self.config.notifications.enable:
            return

        settings = self.config.notifications.settings
        if (event in ['start', 'stop'] and not settings['start_stop']) or \
           (event == 'reboot' and not settings['reboot']) or \
           (event == 'state_change' and not settings['status_change']):
            return

        message_template = self.config.notifications.messages.get(event)
        if not message_template:
            logging.warning(f"Unknown notification type: {event}")
            return

        message = message_template.format(**kwargs)
        tasks = [self.safe_send_message(admin, message) for admin in self.admin_ids]
        await asyncio.gather(*tasks, return_exceptions=True) 