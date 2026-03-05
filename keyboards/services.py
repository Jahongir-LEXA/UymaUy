from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def services_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Uy tozalash", callback_data="svc_cleaning")],
            [InlineKeyboardButton(text="❄️ Konditsioner ustasi", callback_data="svc_ac")],
            [InlineKeyboardButton(text="🚿 Santexnika", callback_data="svc_plumbing")],
            [InlineKeyboardButton(text="⚡ Elektrik", callback_data="svc_electric")],
            [InlineKeyboardButton(text="☀️ Quyosh paneli", callback_data="svc_solar")],
            [InlineKeyboardButton(text="📺 Televizor ustasi", callback_data="svc_tv")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main")],
        ]
    )