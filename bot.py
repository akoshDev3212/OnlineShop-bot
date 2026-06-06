import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web  # Yangi kutubxona qo'shildi
from dotenv import load_dotenv

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# .env faylini yuklash
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Xatolik: .env faylida BOT_TOKEN topilmadi!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render porti uchun HTTP handler
async def handle(request):
    return web.Response(text="Bot is running!")

# Portni ushlab turuvchi server funksiyasi
async def start_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render avtomatik beradigan PORT o'zgaruvchisini o'qiymiz, bo'lmasa 10000 ishlatamiz
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"HTTP server {port}-portda ishga tushdi.")

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
    # 1. HTTP serverni ishga tushiramiz (Render uchun)
    await start_server()
    # 2. Botni polling rejimida ishga tushiramiz
    print("Bot va Server muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi.")