import tkinter
import json
import requests
from datetime import date

class MEAL:
    def __init__(self):
        self.url = ""
        self.ret = ""
        self.breakfast = ""
        self.lunch = ""
        self.dinner = ""
        self.text_id1 = ""
        self.text_id2 = ""
        self.today = date.today().isoformat()

    def clear(self):
        global teacher_meal 
        teacher_meal = tkinter.Canvas(window, width=250, height = 500, background='white', bd=0, highlightthickness=0)
        teacher_meal.place(x=45, y=120)
        global student_meal 
        student_meal = tkinter.Canvas(window, width=250, height = 500, background='white', bd=0, highlightthickness=0)
        student_meal.place(x=305, y=120) 
    def get_student(self):
        #self.url = 'http://127.0.0.1:8888/student'
        self.url = 'http://gosegu.kr:8888/student'
        self.ret = json.loads(requests.get(self.url).text)
        self.breakfast = self.ret[0]
        self.lunch = self.ret[1]
        self.dinner = self.ret[2]
        
    def get_breakfast(self):
        self.clear()
        self.get_student()
        try:
            for i, y in enumerate(self.breakfast[self.today]):
                student_meal.create_text(125, 20 + 30*i, fill='black', font=('Nanum Gothic', 20), text = y)
        except KeyError:
                student_meal.create_text(125, 50, fill='black', font=('Nanum Gothic', 15), text = "오늘은 식단이 없습니다")
    def get_lunch(self, is_teacher=1):
        self.clear()
        if self.text_id1:
            teacher_meal.delete(self.text_id1)
        if self.text_id2:
            student_meal.delete(self.text_id2)
        self.url = 'http://gosegu.kr:8888/teacher'
        self.ret = json.loads(requests.get(self.url).text)
        try:
            for i, y in enumerate(self.ret[self.today]):
                teacher_meal.create_text(125, 20 + 30*i, fill='black', font=('Nanum Gothic', 20), text = y)
        except KeyError:
                teacher_meal.create_text(125, 50, fill='black', font=('Nanum Gothic', 15), text = "오늘은 식단이 없습니다")
        self.get_student()
        try:
            for i, y in enumerate(self.lunch[self.today]):
                student_meal.create_text(125, 20 + 30*i, fill='black', font=('Nanum Gothic', 20), text = y)
        except KeyError:
                student_meal.create_text(125, 50, fill='black', font=('Nanum Gothic', 15), text = "오늘은 식단이 없습니다")
    def get_dinner(self):
        self.clear()
        if self.text_id1:
            teacher_meal.delete(self.text_id1)
        if self.text_id2:
            student_meal.delete(self.text_id2)
        student_meal.delete(self.text_id1)
        self.get_student()
        try:
            for i, y in enumerate(self.dinner[self.today]):
                student_meal.create_text(125, 20 + 30*i, fill='black', font=('Nanum Gothic', 20), text = y)
        except KeyError:
                student_meal.create_text(125, 50, fill='black', font=('Nanum Gothic', 15), text = "오늘은 식단이 없습니다")

command_meal = MEAL()
window = tkinter.Tk()
window.title("KUS school-cafeteria app")
window.geometry("600x800")
label1 = tkinter.Canvas(window, width=200, height = 60, background='white', bd=0, highlightthickness=0)
label1.grid(row = 0, column = 0)
label2 = tkinter.Canvas(window, width=200, height = 60, background='white', bd=0, highlightthickness=0)
label2.create_text(100, 30, text='오늘의 학식', fill='black', font=('Nanum Gothic', 25))
label2.grid(row = 0, column = 1)
label3 = tkinter.Canvas(window, width=200, height = 60, background='white', bd=0, highlightthickness=0)
label3.create_text(100, 30, text=date.today().isoformat(), fill='black', font=('Nanum Gothic', 15))
label3.grid(row = 0, column = 2)

teacher_meal  = tkinter.Canvas(window, width=250, height = 500, background='white', bd=0, highlightthickness=0)
teacher_meal.place(x=45, y=120)
student_meal = tkinter.Canvas(window, width=250, height = 500, background='white', bd=0, highlightthickness=0)
student_meal.place(x=305, y=120)

breakfast_btn = tkinter.Button(window, text="조식", command = lambda: command_meal.get_breakfast())
lunch_btn = tkinter.Button(window, text="중식", command = lambda: command_meal.get_lunch())
dinner_btn = tkinter.Button(window, text="석식", command = lambda: command_meal.get_dinner())

breakfast_btn.place(x=310, y=70)
lunch_btn.place(x=380, y=70)
dinner_btn.place(x=450, y=70)
window.mainloop()
