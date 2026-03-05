from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import SUPPORT_USERNAME
from keyboards.main_menu import main_menu_kb

router = Router()


@router.callback_query(F.data == "menu_support")
async def support_menu(call: CallbackQuery):
    await call.message.edit_text(
        f"Operator bilan bog‘lanish:\n👉 {SUPPORT_USERNAME}",
        reply_markup=main_menu_kb()
    )
    await call.answer()