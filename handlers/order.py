from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    PreCheckoutQuery,
    LabeledPrice,
)
from aiogram.fsm.context import FSMContext

from config import PAYMENT_TOKEN, CURRENCY
from states.order_state import OrderState
from handlers.services import SERVICES
from keyboards.order import pay_kb

router = Router()


@router.callback_query(F.data.startswith("order_start:"))
async def order_start(call: CallbackQuery, state: FSMContext):
    service_key = call.data.split(":", 1)[1]
    if service_key not in SERVICES:
        await call.answer("Xizmat topilmadi", show_alert=True)
        return

    await state.set_state(OrderState.service_key)
    await state.update_data(service_key=service_key)

    await state.set_state(OrderState.location)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Lokatsiya yuborish", request_location=True)]],
        resize_keyboard=True
    )

    await call.message.answer("📍 Lokatsiyani yuboring:", reply_markup=kb)
    await call.answer()


@router.message(OrderState.location)
async def get_location(message: Message, state: FSMContext):
    if not message.location:
        await message.answer("Iltimos, 📍 lokatsiyani tugma orqali yuboring.")
        return

    await state.update_data(location=message.location)
    await state.set_state(OrderState.phone)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Telefon yuborish", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer("📞 Telefon raqamingizni yuboring:", reply_markup=kb)


@router.message(OrderState.phone)
async def get_phone(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Iltimos, 📞 telefonni tugma orqali yuboring.")
        return

    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()

    service_key = data["service_key"]
    service = SERVICES[service_key]

    await message.answer("Buyurtma qabul qilindi ✅", reply_markup=ReplyKeyboardRemove())

    payload = f"{service_key}:{message.from_user.id}"

    await message.answer(
        f"Buyurtma ma'lumotlari:\n\n"
        f"Xizmat: {service['title']}\n"
        f"Telefon: {data['phone']}\n\n"
        f"To‘lov uchun pastdagi tugmani bosing.",
        reply_markup=pay_kb(payload)
    )

    await state.clear()


@router.callback_query(F.data.startswith("pay:"))
async def send_invoice(call: CallbackQuery, bot: Bot):
    payload = call.data.split(":", 1)[1]
    service_key = payload.split(":", 1)[0]

    service = SERVICES.get(service_key)
    if not service:
        await call.answer("Xizmat topilmadi", show_alert=True)
        return

    prices = [LabeledPrice(label=service["title"], amount=service["amount"])]

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=service["title"],
        description=service["desc"],
        provider_token=PAYMENT_TOKEN,
        currency=CURRENCY,
        prices=prices,
        payload=payload,
        start_parameter="uymauy-payment",
        need_name=True,
        need_phone_number=True,
    )
    await call.answer()


@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    service_key = payload.split(":", 1)[0]
    service = SERVICES.get(service_key)

    total = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency

    if not service:
        await message.answer("✅ To‘lov qabul qilindi!")
        return

    await message.answer(
        f"✅ To‘lov muvaffaqiyatli amalga oshirildi!\n\n"
        f"Xizmat: {service['title']}\n"
        f"Summa: {total:,} {currency}\n\n"
        f"Tez orada operator siz bilan bog‘lanadi."
    )