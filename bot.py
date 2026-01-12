from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, BASE_URL

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}

# /start
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("MAX", callback_data="style_max"),
        InlineKeyboardButton("SoundTag", callback_data="style_sound")
    )

    await msg.answer(
        "👋 Привет!\n\n"
        "Здесь ты можешь создать прямую ссылку на сайт.\n\n"
        "ℹ️ Прямые ссылки можно получить через:\n"
        "👉 https://image2url.com\n\n"
        "Выбери стиль:",
        reply_markup=kb
    )

# выбор стиля
@dp.callback_query_handler(lambda c: c.data.startswith("style_"))
async def choose_style(call: types.CallbackQuery):
    style = call.data.split("_")[1]
    users[call.from_user.id] = {"style": style}

    await call.message.answer("🔊 Введи прямую ссылку на музыку:")
    await call.answer()

# ввод данных
@dp.message_handler(lambda m: m.from_user.id in users)
async def handle_input(msg: types.Message):
    uid = msg.from_user.id
    data = users[uid]

    # STYLE 1 — MAX (только музыка)
    if data["style"] == "max":
        music = msg.text.strip()
        link = f"{BASE_URL}/style1.html?music={music}"

        users.pop(uid, None)

    # STYLE 2 — SoundTag (музыка + иконка)
    else:
        if "music" not in data:
            data["music"] = msg.text.strip()
            await msg.answer("🖼 Введи прямую ссылку на иконку:")
            return
        else:
            music = data["music"]
            icon = msg.text.strip()
            link = f"{BASE_URL}/style2.html?music={music}&icon={icon}"

            users.pop(uid, None)

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔗 Открыть", url=link))

    await msg.answer(
        f"✅ Готово!\n\n{link}",
        reply_markup=kb
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
