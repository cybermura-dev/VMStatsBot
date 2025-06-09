from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..config.config_manager import ConfigManager

class KeyboardManager:
    def __init__(self):
        self.config = ConfigManager().config

    def main_menu(self):
        """Main menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="🖥 Управление ВМ", callback_data="vm_control")
        builder.button(text="🔗 Подключение", callback_data="connection_info")
        builder.button(text="⚙️ Настройки", callback_data="settings_menu")
        builder.button(text="📊 Статус", callback_data="current_status")
        builder.button(text="📜 Журнал", callback_data="action_log")
        builder.adjust(2, 2, 1)
        return builder.as_markup()

    def back_button(self, target: str = "main_menu"):
        """Back button keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="◀️ Назад", callback_data=target)
        return builder.as_markup()

    def vm_control_menu(self):
        """VM control menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="▶️ Запустить", callback_data="vm_start")
        builder.button(text="⏹ Остановить", callback_data="vm_stop")
        builder.button(text="🔄 Перезагрузить", callback_data="vm_restart")
        builder.button(text="📋 Состояние", callback_data="vm_state")
        builder.button(text="◀️ Назад", callback_data="main_menu")
        builder.adjust(2, 2, 1)
        return builder.as_markup()

    def settings_menu(self):
        """Settings menu keyboard"""
        builder = InlineKeyboardBuilder()
        notifications = "ВКЛ" if self.config.notifications.enable else "ВЫКЛ"
        interval = self.config.notifications.check_interval
        
        builder.button(text=f"🔔 Уведомления ({notifications})", callback_data="toggle_notifications")
        builder.button(text=f"⏰ Интервал ({interval}s)", callback_data="change_interval")
        builder.button(text="🔧 Типы уведомлений", callback_data="notification_types")
        builder.button(text="🏠 Главное меню", callback_data="main_menu")
        builder.adjust(2, 1)
        return builder.as_markup()

    def notification_types_menu(self):
        """Notification types menu keyboard"""
        builder = InlineKeyboardBuilder()
        settings = self.config.notifications.settings
        
        builder.button(
            text=f"{'✅' if settings['start_stop'] else '❌'} Запуск/Остановка",
            callback_data="toggle_start_stop"
        )
        builder.button(
            text=f"{'✅' if settings['reboot'] else '❌'} Перезагрузка",
            callback_data="toggle_reboot"
        )
        builder.button(
            text=f"{'✅' if settings['status_change'] else '❌'} Смена статуса",
            callback_data="toggle_status_change"
        )
        builder.button(text="◀️ Назад", callback_data="settings_menu")
        builder.adjust(1)
        return builder.as_markup()

    def interval_selection_menu(self):
        """Interval selection menu keyboard"""
        builder = InlineKeyboardBuilder()
        intervals = [10, 30, 60, 120, 300, 600]
        
        for interval in intervals:
            label = f"{interval}s" if interval < 60 else f"{interval//60}m"
            builder.button(text=label, callback_data=f"set_interval_{interval}")
            
        builder.button(text="◀️ Назад", callback_data="settings_menu")
        builder.adjust(3, 3, 1)
        return builder.as_markup()

    def connection_menu(self):
        """Connection menu keyboard"""
        builder = InlineKeyboardBuilder()
        builder.button(text="🔒 Показать пароль", callback_data="show_password")
        builder.button(text="📋 RDP файл", callback_data="get_rdp_file")
        builder.button(text="◀️ Назад", callback_data="main_menu")
        builder.adjust(2, 1)
        return builder.as_markup() 