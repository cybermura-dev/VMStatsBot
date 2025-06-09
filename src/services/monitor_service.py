import asyncio
import logging
from typing import Optional
from aiogram import Bot
from .vm_service import VMService
from .notification_service import NotificationService
from ..config.config_manager import ConfigManager

class MonitorService:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = ConfigManager().config
        self.vm_service = VMService()
        self.notification_service = NotificationService(bot)
        self.last_state: Optional[str] = None
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Start VM monitoring"""
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logging.info("VM monitoring started")

    async def stop(self):
        """Stop VM monitoring"""
        if not self._running:
            return
        
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logging.info("VM monitoring stopped")

    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self._running:
            try:
                current_state = await self.vm_service.get_state()
                
                if self.last_state and current_state != self.last_state:
                    await self.notification_service.send_notification(
                        'state_change',
                        vm_name=self.config.vm.name,
                        old_state=self.last_state,
                        new_state=current_state
                    )
                
                self.last_state = current_state
                await asyncio.sleep(self.config.notifications.check_interval)
                
            except Exception as e:
                logging.error(f"VM monitoring error: {str(e)}", exc_info=True)
                await asyncio.sleep(5)