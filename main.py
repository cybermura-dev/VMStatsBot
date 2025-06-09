import asyncio
import logging
import sys
from signal import SIGINT, SIGTERM
from aiogram import Bot, Dispatcher
from src.config.config_manager import ConfigManager
from src.services.monitor_service import MonitorService
from src.handlers import base, vm_control, settings, connection, action_log

async def shutdown(dp: Dispatcher, monitor: MonitorService, loop: asyncio.AbstractEventLoop):
    """Graceful shutdown"""
    logging.info("\nShutting down...")
    await monitor.stop()
    await dp.bot.session.close()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def main():
    """Main application function"""
    config = ConfigManager().config
    
    logging.basicConfig(
        level=getattr(logging, config.logging.level),
        format=config.logging.format
    )
    
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()
    
    dp.include_router(base.router)
    dp.include_router(vm_control.router)
    dp.include_router(settings.router)
    dp.include_router(connection.router)
    dp.include_router(action_log.router)

    monitor = MonitorService(bot)
    
    loop = asyncio.get_event_loop()
    if sys.platform != 'win32':
        for signal in [SIGINT, SIGTERM]:
            loop.add_signal_handler(
                signal,
                lambda: asyncio.create_task(shutdown(dp, monitor, loop))
            )
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        
        await monitor.start()
        
        await dp.start_polling(bot)
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    except Exception as e:
        logging.critical(f"Critical error: {e}")
    finally:
        await shutdown(dp, monitor, loop)
        if not loop.is_closed():
            await loop.shutdown_asyncgens()
            loop.close()

if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user") 