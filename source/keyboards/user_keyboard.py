from data.models import (
    Teacher,
    Subject,
    Classroom
)

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)


async def user_menu_kb():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add("📚 Предметы", "👨‍🏫 Учителя")
    keyboard.add("🏫 Кабинеты", "📆 Расписание")
    return keyboard


async def teachers_kb(teachers_data: list[Teacher], page: int = 1, items_per_page: int = 15):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton(
            "✏️ Добавить",
            callback_data=f"teachers:{page}:add"
        )
    )
    next_page = page + 1
    previous_page = page - 1
    if teachers_data:
        # Разбитие данных на чанки для отображения на странице
        kb_data = [teachers_data[i:i+items_per_page] for i in range(0, len(teachers_data), items_per_page)]
        for teacher in kb_data[previous_page]:
            keyboard.add(
                InlineKeyboardButton(
                    teacher.name, callback_data=f"teachers:{page}:{teacher.teacher_id}"
                )
            )
        if next_page > len(kb_data):
            next_page = 1
        if previous_page == 0:
            previous_page = len(kb_data)
        keyboard.add(
            InlineKeyboardButton(
                "⬅️",
                callback_data=f"teachers:{previous_page}:view"
            ),
            InlineKeyboardButton(
                f"{page}/{len(kb_data)}",
                callback_data="*"
            ),
            InlineKeyboardButton(
                "➡️",
                callback_data=f"teachers:{next_page}:view"
            )
        )
    return keyboard


async def subjects_kb(subjects_data: list[Subject], page: int = 1, items_per_page: int = 15):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton(
            "✏️ Добавить",
            callback_data=f"subjects:{page}:add"
        )
    )
    next_page = page + 1
    previous_page = page - 1
    if subjects_data:
        kb_data = [subjects_data[i:i+items_per_page] for i in range(0, len(subjects_data), items_per_page)]
        for subject in kb_data[previous_page]:
            keyboard.add(
                InlineKeyboardButton(
                    subject.name,
                    callback_data=f"subjects:{page}:{subject.subject_id}"
                )
            )
        if next_page > len(kb_data):
            next_page = 1
        if previous_page == 0:
            previous_page = len(kb_data)
        keyboard.add(
            InlineKeyboardButton(
                "⬅️",
                callback_data=f"subjects:{previous_page}:view"
            ),
            InlineKeyboardButton(
                f"{page}/{len(kb_data)}",
                callback_data="*"
            ),
            InlineKeyboardButton(
                "➡️",
                callback_data=f"subjects:{next_page}:view"
            )
        )
    return keyboard


async def classrooms_kb(classrooms_data: list[Classroom], page: int = 1, items_per_page: int = 15):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton(
            "✏️ Добавить", callback_data=f"classrooms:{page}:add"
        )
    )
    next_page = page + 1
    previous_page = page - 1
    if classrooms_data:
        kb_data = [classrooms_data[i:i+items_per_page] for i in range(0, len(classrooms_data), items_per_page)]
        for classroom in kb_data[previous_page]:
            keyboard.add(
                InlineKeyboardButton(
                    classroom.number,
                    callback_data=f"classrooms:{page}:{classroom.classroom_id}"
                )
            )
        if next_page > len(kb_data):
            next_page = 1
        if previous_page == 0:
            previous_page = len(kb_data)
        keyboard.add(
            InlineKeyboardButton(
                "⬅️",
                callback_data=f"classrooms:{previous_page}:view"
            ),
            InlineKeyboardButton(
                f"{page}/{len(kb_data)}",
                callback_data="*"
            ),
            InlineKeyboardButton(
                "➡️",
                callback_data=f"classrooms:{next_page}:view"
            )
        )
    return keyboard


async def schedule_kb():
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton(
            "✏️ Добавить", callback_data="schedule:add"
        ),
        InlineKeyboardButton(
            "🧮 Изменить", callback_data="schedule:edit"
        ),
        InlineKeyboardButton(
            "🗑 Удалить", callback_data="schedule:remove"
        )
    )
    return keyboard


async def customizable_kb(button_data, button_type, row_width=2):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    buttons = []
    for button_text in button_data.keys():
        if button_type == "url":
            buttons.append(
                InlineKeyboardButton(
                    button_text,
                    url=button_data.get(button_text)
                )
            )
        if button_type == "callback":
            buttons.append(
                InlineKeyboardButton(
                    button_text,
                    callback_data=button_data.get(button_text)
                )
            )
    keyboard.add(*buttons)
    return keyboard
