from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin_state(StatesGroup):
    login = State()
    password = State()


class Student_state(StatesGroup):
    name = State()
    student_id = State()
    ball = State()
    correct = State()
    not_correct = State()


class update_Student_state(StatesGroup):
    student_id = State()
    ball = State()
    correct = State()
    not_correct = State()


class delete_Student(StatesGroup):
    student_id = State()


class User(StatesGroup):
    student_id = State()
