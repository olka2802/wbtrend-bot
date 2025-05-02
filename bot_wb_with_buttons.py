
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import openai

# Уровень логирования
logging.basicConfig(level=logging.INFO)

# Токен Telegram-бота и ключ OpenAI
TOKEN = "7494917907:AAH8yaouAkXZpHkDW9ZspMk75aAVD2wCK3M"
openai.api_key = "sk-..."

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура с кнопками
main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Предложи нишу", callback_data="suggest_niche")],
    [InlineKeyboardButton(text="Анализ товара", callback_data="analyze_niche")]
])

# Обработка команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я помогу тебе с Wildberries.

Выбери действие:",
        reply_markup=main_keyboard
    )

# Обработка кнопок
@dp.callback_query_handler(lambda c: c.data == "suggest_niche")
async def suggest_niche(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Напиши тему или сферу — я предложу идеи ниш.")
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == "analyze_niche")
async def analyze_niche(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Напиши название ниши, которую нужно проанализировать.")
    await bot.answer_callback_query(callback_query.id)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
