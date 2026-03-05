from aiogram import Router, Bot, F
from aiogram.types import (
    Message,
    PreCheckoutQuery,
    CallbackQuery,
    LabeledPrice
)
from config import PAYMENT_TOKEN

router = Router()


SERVICES = {
    "pay_cleaning": {
        "title": "Uy tozalash xizmati",
        "description": "Professional uy tozalash",
        "price": 120_000_00
    },
    "pay_ac": {
        "title": "Konditsioner xizmati",
        "description": "Konditsioner o‘rnatish / ta'mirlash",
        "price": 180_000_00
    },
    "pay_plumbing": {
        "title": "Santexnika xizmati",
        "description": "Suv tizimi ta'miri",
        "price": 150_000_00
    },
    "pay_electric": {
        "title": "Elektrik xizmati",
        "description": "Elektr montaj ishlari",
        "price": 170_000_00
    },
    "pay_solar": {
        "title": "Quyosh paneli",
        "description": "Quyosh paneli o‘rnatish",
        "price": 300_000_00
    },
    "pay_tv": {
        "title": "Televizor xizmati",
        "description": "TV ta'miri",
        "price": 140_000_00
    },
}


@router.callback_query(F.data.startswith("pay_"))
async def payment_func(call: CallbackQuery, bot: Bot):

    service = SERVICES.get(call.data)

    if not service:
        return await call.answer("Xizmat topilmadi", show_alert=True)

    prices = [
        LabeledPrice(
            label=service["title"],
            amount=service["price"]
        )
    ]

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=service["title"],
        description=service["description"],
        provider_token=PAYMENT_TOKEN,
        currency="UZS",
        prices=prices,
        payload=call.data,
        start_parameter="service-payment",
        need_name=True,
        need_phone_number=True,
    )

    await call.answer()


@router.pre_checkout_query()
async def check_query(query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=query.id,
        ok=True
    )


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):

    payload = message.successful_payment.invoice_payload
    service = SERVICES.get(payload)

    total = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency

    await message.answer(
        f"✅ To‘lov muvaffaqiyatli!\n\n"
        f"Xizmat: {service['title']}\n"
        f"Summa: {total:,} {currency}\n\n"
        f"Tez orada operator siz bilan bog‘lanadi."
    )