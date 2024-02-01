from tortoise import fields
from tortoise.models import Model


class Teacher(Model):
    teacher_id = fields.IntField(pk=True)
    name = fields.CharField(50)


class Subject(Model):
    subject_id = fields.IntField(pk=True)
    name = fields.CharField(50)
    teachers = fields.ManyToManyField("models.Teacher", related_name="subjects")


class Classroom(Model):
    classroom_id = fields.IntField(pk=True)
    number = fields.IntField(unique=True)
    capacity = fields.IntField()  # Вместимость кабинета


class Schedule(Model):
    schedule_id = fields.IntField(pk=True)
    subject = fields.ForeignKeyField("models.Subject", related_name="schedules")
    classroom = fields.ForeignKeyField("models.Classroom", related_name="schedules")
    lesson_date = fields.DateField()  # Дата проведения занятия
    is_active = fields.BooleanField(default=True)  # Флаг активности


class User(Model):
    user_id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField()
    first_name = fields.CharField(max_length=64)
