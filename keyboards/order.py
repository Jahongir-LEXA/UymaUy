from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def order_actions_kb(service_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Buyurtma berish", callback_data=f"order_start:{service_key}")],
            [InlineKeyboardButton(text="⬅️ Xizmatlar", callback_data="back_services")],
        ]
    )


def pay_kb(payload: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Click orqali to‘lash", callback_data=f"pay:{payload}")],
        ]
    )