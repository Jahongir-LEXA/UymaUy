from aiogram.fsm.state import StatesGroup, State


class OrderState(StatesGroup):
    service_key = State()
    location = State()
    phone = State()