# - *- coding: utf- 8 - *-
# Импорт необходимых модулей и классов
from data.models import Classroom
from keyboards.user_keyboard import (
    classrooms_kb,
    customizable_kb
)
from loader import bot, dp
from states.user_states import ClassroomAddState

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

# Обработчик сообщений для команды "🏫 Кабинеты"
@dp.message_handler(text="🏫 Кабинеты", state="*")
async def classrooms_handler(message: Message, state: FSMContext):
    # Завершение текущего состояния (если оно есть)
    await state.finish()
    # Отправка сообщения со списком кабинетов
    await message.answer("<b>Список кабинетов:</b>",
                        reply_markup=await classrooms_kb(await Classroom.all()))

# Обработчик callback-запросов для навигации по кабинетам
@dp.callback_query_handler(text_startswith="classrooms:", state="*")
async def classrooms_call_handler(callback: CallbackQuery, state: FSMContext):
    # Завершение текущего состояния
    await state.finish()
    # Разбиение данных callback на части
    callback_handler_type, page, operation = callback.data.split(":")
    
    # Обработка просмотра кабинетов
    if operation == "view":
        try:
            # Изменение сообщения для отображения другой страницы списка кабинетов
            return await bot.edit_message_reply_markup(
                callback.from_user.id,
                callback.message.message_id,
                reply_markup=await classrooms_kb(await Classroom.all(), page=int(page))
            )
        except MessageNotModified:
            # Обработка исключения, если страница не изменена
            return await callback.answer("Мы на той же страничке)")

    # Обработка добавления нового кабинета
    elif operation == "add":
        new_text = "<b>Отправь номер класса с 1 по 150</b>"
        await ClassroomAddState.classroom_number.set()

    # Обработка запроса информации о конкретном кабинете
    elif operation.isdigit():
        classroom = await Classroom.get(classroom_id=operation)
        new_text = f"🆔: <b>{classroom.number}</b>\n" \
                   f"🧑‍🎓 <b>Вместимость:</b> {classroom.capacity}"
    await callback.message.edit_text(
        new_text,
        reply_markup=await customizable_kb({"👈🏻 Назад": f"classrooms:{page}:view"}, "callback")
    )

# Обработчик сообщений для добавления номера кабинета
@dp.message_handler(lambda message: message.text.isdigit(), state=ClassroomAddState.classroom_number)
async def classrooms_add_name_handler(message: Message, state: FSMContext):
    classroom_number = int(message.text)
    # Проверка корректности номера кабинета
    if classroom_number < 1 and classroom_number > 150:
        return await message.answer("Повторите ввод. Кабинеты начинаются с 1 и заканчиваются 150!")
    # Проверка наличия кабинета с таким номером
    classroom = await Classroom.get_or_none(number=classroom_number)
    if classroom:
        return await message.answer("Повторите ввод. Кабинет с таким номером существует!")
    await state.update_data(classroom_number=classroom_number)
    await ClassroomAddState.next()
    await message.answer("Напиши вместимость класса >0")

# Обработчик сообщений для отклонения ввода, если он не является числом
@dp.message_handler(lambda message: not message.text.isdigit(), state=ClassroomAddState.classroom_capacity)
async def reject_add_name_handler(message: Message, state: FSMContext):
    return await message.answer("Введите число.")

# Обработчик сообщений для добавления вместимости кабинета
@dp.message_handler(lambda message: message.text.isdigit(), state=ClassroomAddState.classroom_capacity)
async def classrooms_add_teachers_handler(message: Message, state: FSMContext):
    classroom_capacity = int(message.text)
    classroom_number = (await state.get_data()).get("classroom_number")
    # Проверка корректности вместимости
    if classroom_capacity < 1:
        return await message.answer("Повторите ввод. Кабинет имеет вместимость <b>минимум 1</b>!")
    # Создание нового кабинета в базе данных
    await Classroom.create(number=classroom_number, capacity=classroom_capacity)
    await message.answer("<b>Успешно добавил!</b>")
    # Возврат к списку кабинетов
    await classrooms_handler(message, state)

# Обработчик сообщений для отклонения ввода вместимости, если он не является числом
@dp.message_handler(lambda message: not message.text.isdigit(), state=ClassroomAddState.classroom_capacity)
async def reject_add_teachers_handler(message: Message, state: FSMContext):
    return await message.answer("Введите число.")
