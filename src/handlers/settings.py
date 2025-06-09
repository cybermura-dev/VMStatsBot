from aiogram import F, Router
from aiogram.types import CallbackQuery
from ..config.config_manager import ConfigManager
from ..keyboards.keyboards import KeyboardManager

router = Router()
config_manager = ConfigManager()
keyboards = KeyboardManager()

@router.callback_query(F.data == "settings_menu")
async def show_settings(call: CallbackQuery):
    """Show settings menu"""
    await call.message.edit_text("⚙️ Настройки:", reply_markup=keyboards.settings_menu())

@router.callback_query(F.data == "notification_types")
async def show_notification_types(call: CallbackQuery):
    """Show notification types menu"""
    await call.message.edit_text("🔧 Типы уведомлений:", reply_markup=keyboards.notification_types_menu())

@router.callback_query(F.data == "change_interval")
async def change_check_interval(call: CallbackQuery):
    """Change check interval"""
    await call.message.edit_text(
        "⏰ Выберите интервал проверки:",
        reply_markup=keyboards.interval_selection_menu()
    )

@router.callback_query(F.data.startswith("set_interval_"))
async def set_interval(call: CallbackQuery):
    """Set check interval"""
    interval = int(call.data.split("_")[2])
    config = config_manager.config
    config.notifications.check_interval = interval
    config_manager.save_config()
    await call.answer(f"Интервал установлен: {interval} секунд")
    await show_settings(call)

@router.callback_query(F.data.startswith("toggle_"))
async def toggle_setting(call: CallbackQuery):
    """Toggle notification settings"""
    toggle_data = call.data.split("_")
    action = toggle_data[1]
    config = config_manager.config
    
    if action == "notifications":
        config.notifications.enable = not config.notifications.enable
        await call.answer(
            "Уведомления " + ("включены" if config.notifications.enable else "выключены")
        )
        await show_settings(call)
    
    elif action == "start" and len(toggle_data) > 2 and toggle_data[2] == "stop":
        config.notifications.settings['start_stop'] = not config.notifications.settings['start_stop']
        await call.answer("Настройки уведомлений обновлены")
        await show_notification_types(call)
    
    elif action == "status" and len(toggle_data) > 2 and toggle_data[2] == "change":
        config.notifications.settings['status_change'] = not config.notifications.settings['status_change']
        await call.answer("Настройки уведомлений обновлены")
        await show_notification_types(call)
    
    elif action == "reboot":
        config.notifications.settings['reboot'] = not config.notifications.settings['reboot']
        await call.answer("Настройки уведомлений обновлены")
        await show_notification_types(call)
    
    else:
        await call.answer(f"Неизвестная настройка: {call.data}", show_alert=True)
        return
    
    config_manager.save_config() 