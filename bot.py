import os
import asyncio
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

class NicheForm(StatesGroup):
    category = State()
    budget = State()
    competition = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Анализ ниши")]], resize_keyboard=True)
    await message.answer("Привет! Я бот, который поможет тебе с нишей для Wildberries.", reply_markup=keyboard)
    await state.clear()

@router.message(F.text == "Анализ ниши")
async def analyze_niche_start(message: types.Message, state: FSMContext):
    await message.answer("Введите категорию товара (например: товары для дома, спорт, одежда и т.д.)")
    await state.set_state(NicheForm.category)

@router.message(NicheForm.category)
async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Какой у вас примерный бюджет на старт? (например: до 50 000 ₽, до 200 000 ₽ и т.д.)")
    await state.set_state(NicheForm.budget)

@router.message(NicheForm.budget)
async def process_budget(message: types.Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await message.answer("Есть ли конкуренты, на которых вы ориентируетесь или хотите обойти?")
    await state.set_state(NicheForm.competition)

@router.message(NicheForm.competition)
async def process_competition(message: types.Message, state: FSMContext):
    await state.update_data(competition=message.text)
    data = await state.get_data()

    prompt = f"""Предложи прибыльную нишу для продажи на Wildberries.
Категория: {data['category']}
Бюджет: {data['budget']}
Конкуренты: {data['competition']}"""

    await message.answer("Анализирую...")
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        niche = response.choices[0].message.content
        await message.answer(f"Вот что я нашёл: {niche}")
    except Exception as e:
        await message.answer(f"Произошла ошибка при обращении к OpenAI: {e}")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
