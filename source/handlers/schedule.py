# - *- coding: utf- 8 - *-
# Импорт модулей и классов
from data.models import (
    Classroom,
    Schedule,
    Subject
)
from datetime import date
from keyboards.user_keyboard import (
    schedule_kb,
    customizable_kb
)
from loader import dp
from states.user_states import (
    ScheduleAddState,
    ScheduleEditState,
    ScheduleDeleteState
)

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

# Обработчик сообщения для просмотра расписания
@dp.message_handler(text="📆 Расписание", state="*")
async def schedule_handler(message: Message, state: FSMContext):
    await state.finish()
    schedules = await Schedule.filter(
        lesson_date=date.today(),
        is_active=True
    ).prefetch_related("subject", "classroom", "subject__teachers")
    schedule_text = "<b>Расписание на сегодня:</b>\n\n"
    for schedule in schedules:
        teachers = ", ".join([teacher.name for teacher in schedule.subject.teachers])
        schedule_text += f"Расписание #{schedule.schedule_id}\n" \
                         f"📚 Предмет: {schedule.subject.name}\n" \
                         f"👨‍🏫 Учитель(-я): {teachers}\n" \
                         f"🏫 Кабинет № {schedule.classroom.number}\n\n"
    await message.answer(schedule_text, reply_markup=await schedule_kb())

# Обработчик callback-запросов для управления расписанием
@dp.callback_query_handler(text_startswith="schedule:", state="*")
async def schedule_call_handler(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    callback_hander_type, operation = callback.data.split(":")
    if operation == "back":
        await callback.message.delete()
        return await schedule_handler(callback.message, state)
    elif operation == "add":
        await ScheduleAddState.schedule_subject.set()
        new_text = "<b>Выбери предмет на клавиатуре</b>"
        subjects = await Subject.all()
        button_data = {subject.name: subject.subject_id for subject in subjects}
    else:
        if operation == "edit":
            await ScheduleEditState.schedule_id.set()
        if operation == "remove":
            await ScheduleDeleteState.schedule_id.set()
        new_text = "<b>Выбери #номер расписания на клавиатуре</b>\n\n❗️ - Скрыты"
        schedules = await Schedule.all()
        button_data = {}
        for schedule in schedules:
            button_text = ("" if schedule.is_active else "❗️ ") + f"#{schedule.schedule_id}"
            button_data.update({button_text: schedule.schedule_id})
    button_data["👈🏻 Назад"] = "schedule:back"
    await callback.message.edit_text(
        new_text,
        reply_markup=await customizable_kb(button_data, "callback", row_width=1)
    )

# Обработчик callback для выбора предмета при добавлении расписания
@dp.callback_query_handler(state=ScheduleAddState.schedule_subject)
async def choose_teacher(callback: CallbackQuery, state: FSMContext):
    subject = callback.data
    await state.update_data(schedule_subject=subject)
    text = "<b>Выбери кабинет на клавиатуре</b>"
    classrooms = await Classroom.all()
    button_data = {}
    for classroom in classrooms:
        button_data.update({f"#{classroom.number}": classroom.classroom_id})
    button_data["👈🏻 Назад"] = "schedule:back"
    await callback.message.edit_text(
        text,
        reply_markup=await customizable_kb(button_data, "callback", row_width=1)
    )
    await ScheduleAddState.next()

# Обработчик callback для выбора кабинета при добавлении расписания
@dp.callback_query_handler(state=ScheduleAddState.schedule_classroom)
async def choose_classroom(callback: CallbackQuery, state: FSMContext):
    classroom = callback.data
    await state.update_data(schedule_classroom=classroom)
    await callback.message.edit_text(
        f"<b>Введи дату проведения занятия</b>\n\nПример: {date.today()}"
    )
    await ScheduleAddState.next()

# Обработчик сообщения для добавления расписания
@dp.message_handler(state=ScheduleAddState.lesson_date)
async def add_schedule(message: Message, state: FSMContext):
    lesson_date = message.text
    state_data = await state.get_data()
    await state.finish()
    await Schedule.create(
        subject=await Subject.get(subject_id=state_data["schedule_subject"]),
        classroom=await Classroom.get(classroom_id=state_data["schedule_classroom"]),
        lesson_date=lesson_date
    )
    await message.answer("Расписание добавлено!")
    await schedule_handler(message, state)

# Обработчик callback для выбора расписания для редактирования
@dp.callback_query_handler(state=ScheduleEditState.schedule_id)
async def select_schedule_to_edit(callback: CallbackQuery, state: FSMContext):
    schedule_id = callback.data
    await state.update_data(schedule_id=schedule_id)
    subjects = await Subject.all()
    button_data = {}
    for subject in subjects:
        button_data.update({subject.name: subject.subject_id})
    button_data["👈🏻 Назад"] = "schedule:back"
    await callback.message.edit_text(
        "<b>Выбери новый предмет на клавиатуре</b>",
        reply_markup=await customizable_kb(button_data, "callback", row_width=1)
    )
    await ScheduleEditState.schedule_subject.set()

# Обработчик callback для изменения кабинета при редактировании расписания
@dp.callback_query_handler(state=ScheduleEditState.schedule_subject)
async def change_classroom(callback: CallbackQuery, state: FSMContext):
    schedule_subject = callback.data
    await state.update_data(schedule_subject=schedule_subject)
    classrooms = await Classroom.all()
    button_data = {}
    for classroom in classrooms:
        button_data.update({classroom.number: classroom.classroom_id})
    button_data["👈🏻 Назад"] = "schedule:back"
    await callback.message.edit_text(
        "<b>Выбери новый кабинет на клавиатуре</b>",
        reply_markup=await customizable_kb(button_data, "callback", row_width=1)
    )
    await ScheduleEditState.schedule_classroom.set()

# Обработчик callback для изменения даты при редактировании расписания
@dp.callback_query_handler(state=ScheduleEditState.schedule_classroom)
async def change_date(callback: CallbackQuery, state: FSMContext):
    schedule_classroom = callback.data
    await state.update_data(schedule_classroom=schedule_classroom)
    today = date.today()
    await callback.message.edit_text(
        f"<b>Введи новую дату проведения занятия</b>\n\nПример: {today}"
    )
    await ScheduleEditState.lesson_date.set()

# Обработчик сообщения для обновления расписания
@dp.message_handler(state=ScheduleEditState.lesson_date)
async def update_schedule(message: Message, state: FSMContext):
    state_data = await state.get_data()
    schedule_id = state_data.get("schedule_id")
    schedule = await Schedule.get(schedule_id=schedule_id)
    schedule.subject_id = state_data.get("schedule_subject")
    schedule.classroom_id = state_data.get("schedule_classroom")
    schedule.lesson_date = message.text
    await schedule.save()
    await state.finish()
    await message.answer("Расписание обновлено.")
    await schedule_handler(message, state)

# Обработчик callback для удаления/деактивации расписания
@dp.callback_query_handler(state=ScheduleDeleteState.schedule_id)
async def delete_schedule(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    schedule_id = int(callback.data)
    schedule = await Schedule.get(schedule_id=schedule_id)
    schedule.is_active = not schedule.is_active
    await schedule.save()
    await callback.message.answer("Статус расписания был изменён.")
    await callback.message.delete()
    await schedule_handler(callback.message, state)
