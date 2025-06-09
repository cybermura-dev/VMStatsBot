from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from ..config.config_manager import ConfigManager
from ..keyboards.keyboards import KeyboardManager
from ..services.vm_service import VMService

router = Router()
config = ConfigManager().config
keyboards = KeyboardManager()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command"""
    if message.from_user.id not in config.bot.admin_ids:
        return
    await message.answer("🖥️ Панель управления виртуальной машиной", reply_markup=keyboards.main_menu())

@router.callback_query(F.data == "main_menu")
async def return_to_main(call: CallbackQuery):
    """Return to main menu"""
    await call.message.edit_text("Главное меню:", reply_markup=keyboards.main_menu())

@router.callback_query(F.data == "vm_control")
async def show_vm_control(call: CallbackQuery):
    """Show VM control menu"""
    await call.message.edit_text("🚀 Управление ВМ:", reply_markup=keyboards.vm_control_menu())

@router.callback_query(F.data == "current_status")
async def show_status(call: CallbackQuery):
    """Show current system status"""
    vm_service = VMService()
    stats = await vm_service.get_system_stats()
    
    status_text = (
        f"📊 <b>Статус системы</b>\n\n"
        f"<b>Виртуальная машина:</b>\n"
        f"• Имя: {config.vm.name}\n"
        f"• Состояние: {stats['state']}\n"
        f"• Время работы: {stats['uptime']}\n\n"
        f"<b>Хост-сервер:</b>\n"
        f"• Загрузка CPU: {stats['cpu_usage']}\n"
        f"• Использование памяти: {stats['memory_usage']}\n"
        f"• Время: {stats['current_time']}"
    )
    
    await call.message.edit_text(
        status_text,
        reply_markup=keyboards.back_button(),
        parse_mode="HTML"
    ) 