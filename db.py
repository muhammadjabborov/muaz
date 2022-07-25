from datetime import date
import sqlite3


from aiohttp import TraceRequestChunkSentParams
from settings import data_path


class Student_admin:
    def __init__(self, data_path) -> None:
        self.connection = sqlite3.connect(data_path)
        self.cursor = self.connection.cursor()

    def new_student(self, name, student_id, ball, correct, not_correct):
        with self.connection:
            self.cursor.execute(
                f"""INSERT INTO students (name, student_id, ball, correct, not_correct) \
                    Values ("{name}", {student_id}, {ball}, "{correct}", "{not_correct}")""")
            self.connection.commit()

    def update_student(self, student_id, ball, correct, not_correct):
        try:
            with self.connection:
                self.cursor.execute(f"""UPDATE students set date = {date('now')}, ball = {ball}, \
                    correct = "{correct}", not_correct = "{not_correct}", Where student_id = {student_id}""")
        except:
            print("update_student funksiyasida hatolik bor tez to'gilla")

    def delete_students(self, student_id):
        with self.connection:
            self.cursor.execute(
                f"Delete from students Where student_id = {student_id}")

    def get_students(self):
        with self.connection:
            students_list = self.cursor.execute(
                f"Select name, student_id from students").fetchall()
        if students_list == None:
            print("students_list bo'sh ")
        else:
            return students_list

    def student_exist(self, student_id):
        with self.connection:
            result = None
            result = self.cursor.execute(
                f"Select * from students where student_id = {student_id}").fetchall()
            print(result)
            if result == None or result == []:
                return False
            else:
                return True

    def have_student(self, student_id):
        with self.connection:
            result = None
            result = self.cursor.execute(
                f"Select * from students where student_id = {student_id}").fetchall()
            print(result)
            if result == None or result == []:
                return True
            else:
                return False


class Student_user:
    def __init__(self, data_path) -> None:
        self.connection = sqlite3.connect(data_path)
        self.cursor = self.connection.cursor()

    def get_date(self, student_id):
        with self.connection:
            data_date = None
            data_date = self.cursor.execute(
                f"Select * from students Where student_id = {student_id}").fetchone()
            if data_date == None or data_date == []:
                return "Hali qo'shilmagan"
            else:
                return data_date[2]

    def get_name(self, student_id):
        with self.connection:
            data_name = None
            data_name = self.cursor.execute(
                f"Select * from students Where student_id = {student_id}").fetchone()
            if data_name == None or data_name == []:
                return "Hali qo'shilmagan"
            else:
                return data_name[3]

    def get_ball(self, student_id):
        with self.connection:
            data_ball = None
            data_ball = self.cursor.execute(
                f"Select * from students Where student_id = {student_id}").fetchone()
            if data_ball == None or data_ball == []:
                return "Hali qo'shilmagan"
            else:
                return data_ball[4]

    def get_correct(self, student_id):
        with self.connection:
            data_correct = None
            data_correct = self.cursor.execute(
                f"Select * from students Where student_id = {student_id}").fetchone()
            if data_correct == None or data_correct == []:
                return "Hali qo'shilmagan"
            else:
                return data_correct[5]

    def get_not_correct(self, student_id):
        with self.connection:
            data_not_correct = None
            data_not_correct = self.cursor.execute(
                f"Select * from students Where student_id = {student_id}").fetchone()
            if data_not_correct == None or data_not_correct == []:
                return "Hali qo'shilmagan"
            else:
                return data_not_correct[6]

    def get_student_exist(self, student_id):
        with self.connection:
            result = None
            result = self.cursor.execute(
                f"Select * from students where student_id = {str(student_id)}").fetchone()
            if result == None or result == []:
                return False
            else:
                return True

