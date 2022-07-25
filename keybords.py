from ctypes import resize
from tkinter import Button
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="O'quvchi qo'shish")],
        [KeyboardButton(text="O'quvchini yangilash")],
        [KeyboardButton(text="O'quvchini o'chirib yuborish")],
        [KeyboardButton(text="Barcha o'quvchilarni ko'rish")]
    ],
    resize_keyboard=True
)

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Mening profilm")]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Back")]
    ],
    resize_keyboard=True
)

correct_not = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="To'g'ri javoblar", callback_data="correct")],
        [InlineKeyboardButton(text="Noto'g'ri javoblar", callback_data="not_correct")]
    ],
    resize_keyboard=True
)
