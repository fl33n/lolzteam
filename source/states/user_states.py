from aiogram.dispatcher.filters.state import State, StatesGroup


class TeacherAddState(StatesGroup):
    teacher_name = State()


class SubjectAddState(StatesGroup):
    subject_name = State()
    subject_teachers = State()


class ClassroomAddState(StatesGroup):
    classroom_number = State()
    classroom_capacity = State()


class ScheduleAddState(StatesGroup):
    schedule_subject = State()
    schedule_classroom = State()
    lesson_date = State()


class ScheduleEditState(StatesGroup):
    schedule_id = State()
    schedule_subject = State()
    schedule_classroom = State()
    lesson_date = State()


class ScheduleDeleteState(StatesGroup):
    schedule_id = State()
