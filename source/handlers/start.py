# - *- coding: utf- 8 - *-
# Импорт необходимых модулей и классов
from data.models import User
from keyboards.user_keyboard import user_menu_kb
from loader import dp
from aiogram.types import Message

# Обработчик команды "/start"
@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message):
    # Получение или создание пользователя в базе данных
    user, is_created = await User.get_or_create(
        telegram_id=message.from_id,
        defaults={"first_name": message.from_user.first_name}
    )

    # Сохранение пользователя, если он был только что создан
    if is_created:
        await user.save()

    # Отправка приветственного сообщения пользователю
    await message.answer(f"<b>Доброго времени суток, {user.first_name}</b>",
                         reply_markup=await user_menu_kb())
