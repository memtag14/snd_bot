import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, BASE_URL

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Временное хранилище данных пользователя
users = {}


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("MAX", callback_data="style_max"),
        InlineKeyboardButton("SoundTag", callback_data="style_sound")
    )

    await message.answer(
        "Выбери стиль:",
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data.startswith("style_"))
async def choose_style(call: types.CallbackQuery):
    style = call.data.split("_")[1]
    users[call.from_user.id] = {"style": style}

    if style == "max":
        await call.message.answer("🔊 Введи ссылку на музыку:")
    else:
        await call.message.answer("🔊 Введи ссылку на музыку:")

    await call.answer()


@dp.message_handler(lambda message: message.from_user.id in users)
async def handle_input(message: types.Message):
    user_id = message.from_user.id
    data = users[user_id]

    # STYLE 1 — MAX
    if data["style"] == "max":
        music = message.text.strip()
        link = f"{BASE_URL}/style1.html?music={music}"

    # STYLE 2 — SoundTag
    else:
        if "music" not in data:
            data["music"] = message.text.strip()
            await message.answer("🖼 Введи ссылку на иконку:")
            return
        else:
            music = data["music"]
            icon = message.text.strip()
            link = f"{BASE_URL}/style2.html?music={music}&icon={icon}"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔗 Открыть", url=link)
    )

    await message.answer(
        f"✅ Готово!\n\n{link}",
        reply_markup=keyboard
    )

    # Очищаем данные пользователя
    users.pop(user_id, None)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
