from codeop import CommandCompiler
from email import message
from subprocess import call
from aiogram import types
from aiogram.dispatcher import FSMContext
from click import command
from aiogram.dispatcher.filters.state import StatesGroup, State
from state_class import *
from keybords import admin_menu, user_menu, back, correct_not
from config import dp, bot
from settings import data_path
from state_class import *
from db import Student_admin, Student_user

student_id = None


@dp.message_handler(commands="start")
async def start_bot(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Assalomu aleykum {message.from_user.last_name} {message.from_user.first_name} Muazning botiga hush kelibsiz",
                           reply_markup=user_menu)


@dp.message_handler(regexp="👤 Mening profilm")
async def my_profil_get_id(message: types.Message):
    print("👤 Mening profilm  bosildi")
    await bot.send_message(message.chat.id, "Id ni kiriting")
    await User.next()


@dp.message_handler(state=User.student_id)
async def my_profil(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global student_id
        student_id = data['student_id'] = message.text
        try:
            if Student_user(data_path).get_student_exist(data.get('student_id')):
                date = Student_user(data_path).get_date(data.get('student_id'))
                name = Student_user(data_path).get_name(data.get('student_id'))
                ball = Student_user(data_path).get_ball(data.get('student_id'))
                correct = Student_user(data_path).get_correct(
                    data.get('student_id'))
                not_correct = Student_user(
                    data_path).get_not_correct(data.get('student_id'))
                await bot.send_message(message.chat.id,
                                       f"📈 Blok test ({date}) natijasi: \n👤 {name}\n🆔 Blok raqami: {data.get('student_id')}\n🔃 Jami ball: {ball} ball",
                                       reply_markup=correct_not)
                await state.finish()
            else:
                await bot.send_message(message.chat.id, "Bunday id mavjud emas")
        except:
            await bot.send_message(message.chat.id, "Noto'g'ri belgi kirittingiz!")
            await User.first()


@dp.callback_query_handler(lambda i: i.data == "correct")
async def my_profil_get_id(callback: types.CallbackQuery):
    global student_id
    correct = Student_user(data_path).get_correct(student_id)
    await bot.send_message(callback.message.chat.id, f"✅ To'g'ri kalitlar: {correct}")
    print(f"✅ To'g'ri kalitlar: {correct}")


@dp.callback_query_handler(lambda i: i.data == "not_correct")
async def my_profil_get_id(callback: types.CallbackQuery):
    global student_id
    not_correct = Student_user(data_path).get_not_correct(student_id)
    await bot.send_message(callback.message.chat.id, f"❌ Noto'g'ri kalitlar: {not_correct}")
    print(f"❌ Noto'g'ri kalitlar: {not_correct}")


@dp.message_handler(commands="admin")
async def start_admin(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id == 440036522 or 1305333316 or 803297293:
        await bot.send_message(message.chat.id, "Siz admin bolimiga kirdingiz", reply_markup=admin_menu)
        print("adminga kirdi")
    else:
        await bot.send_message(message.chat.id,
                               "Loginni kiriting", reply_markup=back)
        print("admin_login soraldi")
        await Admin_state.next()


@dp.message_handler(state=Admin_state.login)
async def admin_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "/start komandasini kiriting")
            print("Logindan keyen back ni bosdi")
        else:
            if message.text == "admin":
                data['login'] = message.text
                await bot.send_message(message.chat.id,
                                       "Parolingizni kiriting", reply_markup=back)
                print("admin_password soraldi")
                await Admin_state.next()
            else:
                await bot.send_message(message.chat.id, "Siz loginni noto'g'ri kirittingiz!", reply_markup=back)
                print("login noto'g'ri kirildi")


@dp.message_handler(state=Admin_state.password)
async def admin_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "/start komandasini kiriting")
            print("paroldan keyen back ni bosdi")
        else:
            if message.text == "123":
                data['password'] = message.text
                await bot.send_message(message.chat.id, "Siz admin bo'limiga kirdingiz!", reply_markup=admin_menu)
                print("admin bo'limiga kirdi")
                await state.finish()
            else:
                await bot.send_message(message.chat.id, "Siz parolni noto'g'ri kirittingiz!", reply_markup=back)
                print("parolni notogri terdi")


@dp.message_handler(regexp="O'quvchi qo'shish")
async def add_student_start(message: types.Message):
    await bot.send_message(message.chat.id,
                           "O'quvchining ism sharifini kiriting", reply_markup=back)
    print("oquvchi qoshish ni bosdi")
    await Student_state.next()


@dp.message_handler(state=Student_state.name)
async def get_name_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
            print("backda admin bolimiga qaytdi")
        else:
            data['name'] = message.text
            await bot.send_message(message.chat.id, "O'quvchining id sini kiriting", reply_markup=back)
            print("o'quvchini id sini soradi")
            await Student_state.next()


@dp.message_handler(state=Student_state.student_id)
async def get_id_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
            print("backda admin bolimiga qaytdi")
        else:
            try:
                if Student_admin(data_path).have_student(message.text):
                    data['student_id'] = message.text
                    await bot.send_message(message.chat.id, "O'quvchining umumiy balini kiriting", reply_markup=back)
                    print("oquvchining umumiy balini kiriting soraldi")
                    await Student_state.next()
                else:
                    await bot.send_message(message.chat.id, "Bunday id mavjud, boshqasini kiriting", reply_markup=back)
                    print("umumiy balini notigri kiritti")
            except:
                await bot.send_message(message.chat.id, "Noto'g'ri id kirittingiz!")
                Student_state.student_id


@dp.message_handler(state=Student_state.ball)
async def get_name_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
            print("backda admin bolimiga qaytdi")
        else:
            if message.text.isdigit():
                data['ball'] = message.text
                await bot.send_message(message.chat.id, "O'quvchining to'g'ri javoblarini kiriting", reply_markup=back)
                print("togri javoblari soraldi")
                await Student_state.next()
            else:
                await bot.send_message(message.chat.id, "O'quvchining umumuy balini to'g'ri kiriting",
                                       reply_markup=back)
                print("noto'gri kiritti togri javoblarini")


@dp.message_handler(state=Student_state.correct)
async def get_correct_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
        else:
            data['correct'] = message.text
            await bot.send_message(message.chat.id, "O'quvchining noto'g'ri javoblarini kiriting", reply_markup=back)
            await Student_state.next()


@dp.message_handler(state=Student_state.not_correct)
async def get_not_correct_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
        else:
            data['not_correct'] = message.text
            Student_admin(data_path).new_student(data.get('name'), data.get('student_id'), data.get(
                'ball'), data.get('correct'), data.get('not_correct'))
            await bot.send_message(message.chat.id, "O'quvchi muvaffaqiyatli qo'shildi", reply_markup=admin_menu)
            await state.finish()


@dp.message_handler(regexp="O'quvchini yangilash")
async def update_students(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "O'zgartirmoqchi bo'lgan o'quvchingizni id sini kiriting",
                           reply_markup=back)
    await update_Student_state.next()


@dp.message_handler(state=update_Student_state.student_id)
async def get_id_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if message.text == "🔙 Back":
                await state.finish()
                await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
            else:

                if Student_admin(data_path).student_exist(message.text):
                    data['student_id'] = message.text
                    await bot.send_message(message.chat.id, "O'quvchining balini kiriting", reply_markup=back)
                    await update_Student_state.next()
                else:
                    await bot.send_message(message.chat.id, "Bunday id mavjud emas", reply_markup=back)
        except:
            await bot.send_message(message.chat.id, "Noto'g'ri id kirittingiz!")
            update_Student_state.student_id


@dp.message_handler(state=update_Student_state.ball)
async def get_name_update_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
        else:
            data['ball'] = message.text
            await bot.send_message(message.chat.id, "O'quvchining to'g'ri javoblarini kiriting", reply_markup=back)
            await update_Student_state.next()


@dp.message_handler(state=update_Student_state.correct)
async def get_correct_update_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
        else:
            data['correct'] = message.text
            await bot.send_message(message.chat.id, "O'quvchining noto'g'ri javoblarini kiriting", reply_markup=back)
            await update_Student_state.next()


@dp.message_handler(state=update_Student_state.not_correct)
async def get_not_correct_update_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
        else:
            data['not_correct'] = message.text
            Student_admin(data_path).update_student(data.get('student_id'), data.get(
                'ball'), data.get('correct'), data.get('not_correct'))
            await bot.send_message(message.chat.id, "Siz muvaffaqiyatli o'zgartirdingiz", reply_markup=admin_menu)
            await state.finish()


@dp.message_handler(regexp="O'quvchini o'chirib yuborish")
async def student_delete(message: types.Message):
    await bot.send_message(message.chat.id, "O'chirmoqchi bo'lgan o'quvchingizni id sini kiriting", reply_markup=back)
    await delete_Student.next()


@dp.message_handler(state=delete_Student.student_id)
async def get_student_id_for_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "🔙 Back":
            await state.finish()
            await bot.send_message(message.chat.id, "Siz admin bo'limiga qaytdingiz", reply_markup=admin_menu)
        else:
            try:
                if Student_admin(data_path).student_exist(message.text):
                    data['student_id'] = message.text
                    Student_admin(data_path).delete_students(
                        data.get('student_id'))
                    await bot.send_message(message.chat.id, "O'quvchi muvaffaqiyatli o'chirib yuborildi",
                                           reply_markup=admin_menu)
                    await state.finish()
                else:
                    await bot.send_message(message.chat.id, "Bunday id mavjud emas", reply_markup=back)
            except:
                await bot.send_message(message.chat.id, "Noto'g'ri id kirittingiz!")
                delete_Student.student_id


@dp.message_handler(regexp="Barcha o'quvchilarni ko'rish")
async def see_all_students(message: types.Message):
    get_stud = Student_admin(data_path).get_students()
    for i in get_stud:
        print(i)
        await bot.send_message(message.chat.id, f"Ism sharifi: {i[0]}\nID raqami: {i[1]}", reply_markup=admin_menu)
