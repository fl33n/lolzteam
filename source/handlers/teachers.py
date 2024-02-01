# - *- coding: utf- 8 - *-
# Импорты и объявления
from data.models import Subject, Teacher
from keyboards.user_keyboard import (
    teachers_kb,
    customizable_kb
)
from loader import bot, dp
from states.user_states import TeacherAddState

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

# Обработчик сообщения для отображения списка учителей
@dp.message_handler(text="👨‍🏫 Учителя", state="*")
async def teachers_handler(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Список учителей:</b>",
                        reply_markup=await teachers_kb(await Teacher.all()))

# Обработчик callback-запросов для управления учителями
@dp.callback_query_handler(text_startswith="teachers:", state="*")
async def teachers_call_handler(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    callback_handler_type, page, operation = callback.data.split(":")
    if operation == "view":
        try:
            return await bot.edit_message_reply_markup(
                callback.from_user.id,
                callback.message.message_id,
                reply_markup=await teachers_kb(await Teacher.all(), page=int(page))
            )
        except MessageNotModified:
            return await callback.answer("Мы на той же страничке)")
    elif operation == "add":
        new_text = "<b>Отправь имя учителя</b>"
        await TeacherAddState.teacher_name.set()
    elif operation.isdigit():
        teacher = await Teacher.get(teacher_id=operation)
        subjects = await Subject.filter(teachers=teacher)
        subjects = [subject.name for subject in subjects]
        new_text = f"👨‍🏫 <b>{teacher.name}</b>\n📚 <b>Ведёт предметы:</b> " \
                   f"<code>{(', '.join(subjects) if subjects else 'Отсутствуют')}</code>"
    await callback.message.edit_text(
        new_text,
        reply_markup=await customizable_kb({"👈🏻 Назад": f"teachers:{page}:view"}, "callback")
    )

# Обработчик сообщения для добавления нового учителя
@dp.message_handler(state=TeacherAddState.teacher_name)
async def teachers_add_handler(message: Message, state: FSMContext):
    await state.finish()
    teacher_name = message.text
    await Teacher.create(name=teacher_name)
    await message.answer("<b>Успешно добавил!</b>")
    await teachers_handler(message, state)
