from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛠 Servis", callback_data="menu_services"),
                InlineKeyboardButton(text="📞 Support", callback_data="menu_support"),
            ]
        ]
    )