from aiogram import F, Router
from aiogram.types import CallbackQuery
from ..services.vm_service import VMService
from ..services.notification_service import NotificationService
from ..keyboards.keyboards import KeyboardManager

router = Router()
keyboards = KeyboardManager()

@router.callback_query(F.data.startswith("vm_"))
async def handle_vm_control(call: CallbackQuery, bot):
    """Handle VM control commands"""
    vm_service = VMService()
    notification_service = NotificationService(bot)
    action = call.data.split("_")[1]
    
    if action == "state":
        state = await vm_service.get_state()
        state_text = f"Текущее состояние ВМ: {state}"
        if len(state_text) > 200:
            state_text = state_text[:197] + "..."
        await call.answer(state_text, show_alert=True)
    else:
        try:
            await vm_service.control(action)
            event_name = "reboot" if action == "restart" else action
            await notification_service.send_notification(
                event_name,
                vm_name=vm_service.vm_name
            )
            await call.answer(f"Команда '{action}' выполнена!", show_alert=True)
        except ValueError as e:
            error_msg = str(e)
            if len(error_msg) > 200:
                error_msg = error_msg[:197] + "..."
            await call.answer(error_msg, show_alert=True)
        except Exception as e:
            error_msg = f"Ошибка выполнения команды: {str(e)}"
            if len(error_msg) > 200:
                error_msg = error_msg[:197] + "..."
            await call.answer(error_msg, show_alert=True)
    
    try:
        await call.message.edit_text("🚀 Управление ВМ:", reply_markup=keyboards.vm_control_menu())
    except Exception:
        pass 