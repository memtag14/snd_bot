from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, BASE_URL

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("🔊 Введи прямую ссылку на музыку (.mp3):")

@dp.message_handler()
async def get_music(msg: types.Message):
    music = msg.text.strip()

    link = f"{BASE_URL}/style1.html?music={music}"

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔗 Открыть", url=link))

    await msg.answer(
        f"✅ Готово!\n\n{link}",
        reply_markup=kb
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
