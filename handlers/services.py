from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.main_menu import main_menu_kb
from keyboards.services import services_kb
from keyboards.order import order_actions_kb

router = Router()

SERVICES = {
    "cleaning": {
        "title": "🏠 Uy tozalash",
        "desc": "Professional uy tozalash xizmati.",
        "price_sum": 120_000,
        "amount": 120_000_00,
    },
    "ac": {
        "title": "❄️ Konditsioner ustasi",
        "desc": "O‘rnatish / ta’mirlash / texnik xizmat.",
        "price_sum": 180_000,
        "amount": 180_000_00,
    },
    "plumbing": {
        "title": "🚿 Santexnika",
        "desc": "Sanitariya-tesisat tizimlari o‘rnatish va ta’mirlash.",
        "price_sum": 150_000,
        "amount": 150_000_00,
    },
    "electric": {
        "title": "⚡ Elektrik",
        "desc": "Elektr jihozlarini o‘rnatish, ta’mirlash, almashtirish.",
        "price_sum": 170_000,
        "amount": 170_000_00,
    },
    "solar": {
        "title": "☀️ Quyosh paneli",
        "desc": "Quyosh panellarini o‘rnatish xizmati.",
        "price_sum": 300_000,
        "amount": 300_000_00,
    },
    "tv": {
        "title": "📺 Televizor ustasi",
        "desc": "Televizor diagnostika va ta’mirlash.",
        "price_sum": 140_000,
        "amount": 140_000_00,
    },
}


@router.callback_query(F.data == "menu_services")
async def open_services(call: CallbackQuery):
    await call.message.edit_text("Xizmat turini tanlang:", reply_markup=services_kb())
    await call.answer()


@router.callback_query(F.data == "back_main")
async def back_main(call: CallbackQuery):
    await call.message.edit_text("Asosiy menyu:", reply_markup=main_menu_kb())
    await call.answer()


@router.callback_query(F.data == "back_services")
async def back_services(call: CallbackQuery):
    await call.message.edit_text("Xizmat turini tanlang:", reply_markup=services_kb())
    await call.answer()


@router.callback_query(F.data.startswith("svc_"))
async def show_service(call: CallbackQuery):
    key = call.data.replace("svc_", "")
    service = SERVICES.get(key)
    if not service:
        await call.answer("Xizmat topilmadi", show_alert=True)
        return

    text = (
        f"{service['title']}\n\n"
        f"{service['desc']}\n\n"
        f"Narx: {service['price_sum']:,} so‘m\n\n"
        f"Buyurtma berasizmi?"
    )

    await call.message.edit_text(text, reply_markup=order_actions_kb(service_key=key))
    await call.answer()