from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def start_keyboard():
    static_buttons = InlineKeyboardBuilder()
    static_buttons.add(InlineKeyboardButton(text="Расписание", callback_data=f"rasp"))
    static_buttons.add(InlineKeyboardButton(text="Cделать расписание", callback_data=f"new"))
    static_buttons.add(InlineKeyboardButton(text="Удалить сообщение", callback_data=f"del"))
    return static_buttons.adjust(2).as_markup()

async def back_keyboard():
    static_buttons = InlineKeyboardBuilder()
    static_buttons.add(InlineKeyboardButton(text="Назад", callback_data=f"back"))
    return static_buttons.adjust(1).as_markup()

async def user_keyboard():
    static_buttons = InlineKeyboardBuilder()
    static_buttons.add(InlineKeyboardButton(text="Расписание", callback_data=f"rasp"))
    return static_buttons.adjust(1).as_markup()