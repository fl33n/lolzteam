# - *- coding: utf- 8 - *-
# Импорты и объявления
from data.models import Subject, Teacher
from keyboards.user_keyboard import (
    subjects_kb,
    customizable_kb
)
from loader import bot, dp
from states.user_states import SubjectAddState

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

# Обработчик сообщения для отображения списка предметов
@dp.message_handler(text="📚 Предметы", state="*")
async def subjects_handler(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Список предметов:</b>",
                        reply_markup=await subjects_kb(await Subject.all()))

# Обработчик callback-запросов для управления предметами
@dp.callback_query_handler(text_startswith="subjects:", state="*")
async def subjects_call_handler(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    callback_handler_type, page, operation = callback.data.split(":")
    if operation == "view":
        try:
            return await bot.edit_message_reply_markup(
                callback.from_user.id,
                callback.message.message_id,
                reply_markup=await subjects_kb(await Subject.all(), page=int(page))
            )
        except MessageNotModified:
            return await callback.answer("Мы на той же страничке)")
    elif operation == "add":
        new_text = "<b>Отправь название предмета</b>"
        await SubjectAddState.subject_name.set()
    elif operation.isdigit():
        subject = await Subject.get(subject_id=operation).prefetch_related("teachers")
        teachers = [teacher.name for teacher in subject.teachers]
        new_text = f"📚 <b>{subject.name}</b>\n" \
                   "👨‍🏫 <b>Учителя, ведущие предмет:</b> " \
                   f"<code>{(', '.join(teachers) if teachers else 'Отсутствуют')}</code>"
    await callback.message.edit_text(
        new_text,
        reply_markup=await customizable_kb({"👈🏻 Назад": f"subjects:{page}:view"}, "callback")
    )

# Обработчик сообщения для добавления названия нового предмета
@dp.message_handler(state=SubjectAddState.subject_name)
async def subjects_add_name_handler(message: Message, state: FSMContext):
    subject_name = message.text
    await state.update_data(subject_name=subject_name)
    await SubjectAddState.next()
    teachers_data = await Teacher.all()
    teacher_list = [f"{teacher.teacher_id}. {teacher.name}" for teacher in teachers_data]
    teacher_list = "\n".join(teacher_list)
    await message.answer(
        f"<b>Напиши id учителей которые ведут предмет через запятую:</b>\n\n{teacher_list}"
    )

# Обработчик сообщения для добавления преподавателей предмета
@dp.message_handler(state=SubjectAddState.subject_teachers)
async def subjects_add_teachers_handler(message: Message, state: FSMContext):
    teacher_ids = message.text.split(", ")
    teachers_data = []
    for teacher_id in teacher_ids:
        teacher = await Teacher.get_or_none(teacher_id=teacher_id)
        if teacher:
            teachers_data.append(teacher)
    subject_name = (await state.get_data()).get("subject_name")
    await state.finish()
    subject = await Subject.create(name=subject_name)
    for teacher in teachers_data:
        await subject.teachers.add(teacher)
    await message.answer("<b>Успешно добавил!</b>")
    await subjects_handler(message, state)
