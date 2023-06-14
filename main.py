import tkinter
import json
import requests
from datetime import date
from PIL import Image

class MEAL:
    def __init__(self):
        self.url = ""
        self.ret = ""
        self.breakfast = ""
        self.lunch = ""
        self.dinner = ""
        self.today = date.today().isoformat()

    def clear(self):
        global teacher_meal 
        teacher_meal = tkinter.Canvas(window, width=250, height = 500, background='white', bd=0, highlightthickness=0)
        teacher_meal.place(x=45, y=120)
        global student_meal 
        student_meal = tkinter.Canvas(window, width=250, height = 500, background='white', bd=0, highlightthickness=0)
        student_meal.place(x=305, y=120) 
        teacher_meal.create_text(125, 15, fill='black', font=('Nanum Gothic', 25), text = '교직원')
        student_meal.create_text(125, 15, fill='black', font=('Nanum Gothic', 25), text = '학생')
        
    def get_student(self):
        #self.url = 'http://127.0.0.1:8888/student' -> this is debug for local
        self.url = 'http://gosegu.kr:8888/student'
        self.ret = json.loads(requests.get(self.url).text)
        self.breakfast = self.ret[0]
        self.lunch = self.ret[1]
        self.dinner = self.ret[2]

    def create_meal_text(self, x, y, foo, content):
        foo.create_text(x, y, fill='black', font=('Nanum Gothic', 20), text = content)
        
    def error(self, foo):
        foo.create_text(125, 50, fill = 'black', font=('Nanum Gothic', 15), text = "오늘은 식단이 없습니다")
        
    def refilter(self):
        for x in self.ret:
            tmp = []
            for y in self.ret[x]:
                if "&amp;" in y:
                    y = y.replace("&amp;", "&");
                if "\x0a" in y:
                    y = y.replace("\x0a", "")
                tmp.append(y)
            self.ret[x] = tmp

    def get_breakfast(self):
        self.clear()
        self.get_student()
        try:
            for i, y in enumerate(self.breakfast[self.today]):
                self.create_meal_text(125, 60 + 30 * i, student_meal, y)

        except KeyError:
                self.error(student_meal)

    def get_lunch(self, is_teacher=1):
        self.clear()
        self.url = 'http://gosegu.kr:8888/teacher'
        self.ret = json.loads(requests.get(self.url).text)
        self.refilter()
        try:
            for i, y in enumerate(self.ret[self.today]):
                self.create_meal_text(125, 60 + 30 * i, teacher_meal, y)
        except KeyError:
                self.error(teacher_meal)
        self.get_student()
        try:
            for i, y in enumerate(self.lunch[self.today]):
                self.create_meal_text(125, 60 + 30 * i, student_meal, y)
        except KeyError:
                self.error(student_meal)
                
    def get_dinner(self):
        self.clear()
        self.get_student()
        try:
            for i, y in enumerate(self.dinner[self.today]):
                self.create_meal_text(125, 60 + 30 * i, student_meal, y)
        except KeyError:
                self.error(student_meal)

command_meal = MEAL()
window = tkinter.Tk()
window.title("KUS school-cafeteria app")
window.geometry("600x800")
img = Image.open('./kus2.png')
img_resize = img.resize((60, 60))
img_resize.save('./kus2.png')
imgObj = tkinter.PhotoImage(file = './kus2.png')
label1 = tkinter.Canvas(window, width=200, height = 60, background='white', bd=0, highlightthickness=0)
label1.create_image(30, 30, image=imgObj)
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

teacher_meal.create_text(125, 15, fill='black', font=('Nanum Gothic', 25), text = '교직원')
student_meal.create_text(125, 15, fill='black', font=('Nanum Gothic', 25), text = '학생')
breakfast_btn = tkinter.Button(window, text="조식", command = lambda: command_meal.get_breakfast())
lunch_btn = tkinter.Button(window, text="중식", command = lambda: command_meal.get_lunch())
dinner_btn = tkinter.Button(window, text="석식", command = lambda: command_meal.get_dinner())

breakfast_btn.place(x=200, y=70)
lunch_btn.place(x=270, y=70)
dinner_btn.place(x=340, y=70)
window.mainloop()
