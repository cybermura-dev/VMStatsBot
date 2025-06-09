import os
from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile
from ..config.config_manager import ConfigManager
from ..keyboards.keyboards import KeyboardManager

router = Router()
config = ConfigManager().config
keyboards = KeyboardManager()

@router.callback_query(F.data == "connection_info")
async def show_connection(call: CallbackQuery):
    """Show connection information"""
    connection = config.vm.connection
    text = (
        f"🔌 <b>Данные подключения:</b>\n"
        f"• Адрес: <code>{connection.address}</code>\n"
        f"• Протокол: {connection.protocol}\n"
        f"• Пароль: {'*' * len(connection.password)}"
    )
    await call.message.edit_text(
        text,
        reply_markup=keyboards.connection_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "show_password")
async def reveal_password(call: CallbackQuery):
    """Show connection password"""
    await call.answer(
        f"Пароль: {config.vm.connection.password}",
        show_alert=True
    )

@router.callback_query(F.data == "get_rdp_file")
async def send_rdp_file(call: CallbackQuery):
    """Generate and send RDP connection file"""
    connection = config.vm.connection
    rdp_settings = connection.rdp_settings
    
    rdp_content = [
        f"full address:s:{connection.address}",
        f"username:s:{rdp_settings['username']}",
        "prompt for credentials:i:0",
        f"screen mode id:i:{rdp_settings['screen_mode']}",
        f"desktopwidth:i:{rdp_settings['desktop_width']}",
        f"desktopheight:i:{rdp_settings['desktop_height']}",
        f"session bpp:i:{rdp_settings['session_bpp']}"
    ]
    
    temp_file = "temp_connection.rdp"
    try:
        with open(temp_file, "w") as f:
            f.write("\n".join(rdp_content))
        
        await call.message.answer_document(
            FSInputFile(temp_file, filename=f"{config.vm.name}_connection.rdp"),
            caption="🔗 Файл подключения RDP"
        )
    finally:
        try:
            os.remove(temp_file)
        except:
            pass
    
    await call.answer() 