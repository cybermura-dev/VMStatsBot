from aiogram import F, Router
from aiogram.types import CallbackQuery
from ..services.vm_service import VMService
from ..keyboards.keyboards import KeyboardManager

router = Router()
keyboards = KeyboardManager()

def truncate_log_text(text: str, max_length: int = 4096) -> str:
    """Truncate text to fit Telegram message limits"""
    if len(text) <= max_length:
        return text
    return text[:max_length-100] + "\n\n... (Показаны только последние события)"

@router.callback_query(F.data == "action_log")
async def show_logs(call: CallbackQuery):
    """Show event logs with proper length handling"""
    vm_service = VMService()
    vm_events = await vm_service.get_logs()
    
    if not vm_events:
        log_text = "📜 <b>Журнал событий</b>\n\nНет недавних событий VM в журнале."
    else:
        events_text = f"<pre>{vm_events}</pre>"
        log_text = "📜 <b>Журнал событий VM</b>\n\n" + truncate_log_text(events_text)
    
    await call.message.edit_text(
        log_text,
        reply_markup=keyboards.back_button(),
        parse_mode="HTML"
    ) 