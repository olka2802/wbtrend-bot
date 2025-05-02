
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import openai

# Уровень логирования
logging.basicConfig(level=logging.INFO)

# Токены
TOKEN = "7494917907:AAH8yaouAkXZpHkDW9ZspMk75aAVD2wCK3M"
openai.api_key = "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"

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Состояния пользователей
user_state = {}

# Клавиатура
main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Предложи нишу", callback_data="suggest_niche"),
        InlineKeyboardButton(text="Анализ товара", callback_data="analyze_niche")
    ],
    [
        InlineKeyboardButton(text="Тренды на WB", callback_data="wb_trends"),
        InlineKeyboardButton(text="Помощь", callback_data="help")
    ]
])

# Команда /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я помогу тебе с Wildberries.\n\nВыбери действие:",
        reply_markup=main_keyboard
    )

# Кнопка "Предложи нишу"
@dp.callback_query_handler(lambda c: c.data == "suggest_niche")
async def suggest_niche(callback_query: types.CallbackQuery):
    user_state[callback_query.from_user.id] = "awaiting_sphere"
    await bot.send_message(callback_query.from_user.id, "Напиши сферу, и я предложу ниши.")
    await bot.answer_callback_query(callback_query.id)

# Кнопка "Анализ товара"
@dp.callback_query_handler(lambda c: c.data == "analyze_niche")
async def analyze_niche(callback_query: types.CallbackQuery):
    user_state[callback_query.from_user.id] = "awaiting_niche"
    await bot.send_message(callback_query.from_user.id, "Напиши нишу, и я проанализирую её с помощью ИИ.")
    await bot.answer_callback_query(callback_query.id)

# Кнопка "Тренды"
@dp.callback_query_handler(lambda c: c.data == "wb_trends")
async def wb_trends(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Вот, что сейчас в тренде:\n1. Умные часы\n2. Органайзеры\n3. Маски для сна")
    await bot.answer_callback_query(callback_query.id)

# Кнопка "Помощь"
@dp.callback_query_handler(lambda c: c.data == "help")
async def help_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Если возникли вопросы — пиши сюда: @yourusername")
    await bot.answer_callback_query(callback_query.id)

# Обработка текстовых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get(user_id)

    if state == "awaiting_niche":
        user_state[user_id] = None
        await message.answer("Анализирую нишу...")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты эксперт по маркетплейсу Wildberries."},
                {"role": "user", "content": f"Проанализируй нишу: {message.text}"}
            ],
            max_tokens=500
        )

        result = response['choices'][0]['message']['content']
        await message.answer(result)

    elif state == "awaiting_sphere":
        user_state[user_id] = None
        await message.answer("Генерирую идеи ниш...")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты специалист по выбору ниш для Wildberries."},
                {"role": "user", "content": f"Предложи перспективные ниши в категории: {message.text}"}
            ],
            max_tokens=500
        )

        ideas = response['choices'][0]['message']['content']
        await message.answer(ideas)

# Запуск
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
