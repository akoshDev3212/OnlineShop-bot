import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# .env faylini yuklash
load_dotenv()

# Tokenni .env faylidan o'qish (Kodning boshida tokenni yozib qo'ymang!)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Xatolik: .env faylida BOT_TOKEN topilmadi!")

# Bot va Dispatcher obyektlari
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    web_app_url = "https://onlineshop-ism1.onrender.com/"
    
    web_app_button = InlineKeyboardButton(
        text="TexnoShop'ni ochish 🚀", 
        web_app=WebAppInfo(url=web_app_url)
    )
    
    markup = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])
    
    await message.answer(
        "Assalomu alaykum! TexnoShop do'koniga xush kelibsiz! 🛍\n"
        "Mahsulotlarni ko'rish va xarid qilish uchun pastdagi tugmani bosing.",
        reply_markup=markup
    )

async def main():
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi.")