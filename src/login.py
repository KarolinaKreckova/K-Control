from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pymysql

def clear():
    usernameEntry.delete(0,END)
    passwordEntry.delete(0,END)

def login_user():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Vyplňte všechna pole')

    else:
        try:
            conn = pymysql.connect(host='localhost', user='root')
            mycursor = conn.cursor()
        except:
            messagebox.showerror('Error', 'Připojení se nezdařilo')
            return
        query = 'use uzivatelskaData'
        mycursor.execute(query)
        query = 'select * from uzivatel where username=%s and password=%s'
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Chybné uživatelské jméno nebo heslo')
        else:
            role = row[3]
            if role == 'Admin':
                clear()
                LogIn.destroy()
                import ctvrtaStranaAdmin
            elif role == 'KS':
                clear()
                LogIn.destroy()
                import kontrolorTretiStrana
            elif role == 'OZ':
                clear()
                LogIn.destroy()
                import ObjednavkastranaTri


def user_enter(event):
    if usernameEntry.get() == 'Přihlašovací jméno':
        usernameEntry.delete(0, END)


def password_enter(event):
    if passwordEntry.get() == 'Heslo':
        passwordEntry.delete(0, END)


def hide():
    openEye.config(file='img/eyeClose.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)


def show():
    openEye.config(file='img/eyeOpen.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)

LogIn = Tk()
LogIn.title('Log in')
window_width = 320
window_height = 450
screen_width = LogIn.winfo_screenwidth()
screen_height = LogIn.winfo_screenheight()
#print(screen_width)
#print(screen_height)

x_axis = (screen_width / 2) - (window_width / 2)
y_axis = (screen_height / 2) - (window_height / 2)

LogIn.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_axis), int(y_axis)))
LogIn.resizable(False,False)


#background Image
bgImage = tk.PhotoImage(file='img/background.png')
bgLabel = Label(LogIn, image=bgImage)
bgLabel.pack()
bgLabel.place(x=-310, y=-15)

heading = Label(LogIn, text='Přihlášení', font=('Microsoft Yahei UI Light', 12, 'bold'),
                bg='white', fg='black')
heading.place(x=120, y=190)

#Username
usernameEntry = Entry(LogIn, width=18, font=('Microsoft Yahei UI Light', 9, 'bold'),
                      bd=0, fg='black')
usernameEntry.place(x=83, y=240)
usernameEntry.insert(0, 'Přihlašovací jméno')
usernameEntry.bind('<FocusIn>', user_enter)
frame1 = Frame(LogIn, width=160, height=2, bg='black')
frame1.place(x=83, y=260)

#Password
passwordEntry = Entry(LogIn, width=18, font=('Microsoft Yahei UI Light', 9, 'bold'),
                      bd=0, fg='black',show='*')
passwordEntry.place(x=83, y=290)
passwordEntry.insert(0, 'Heslo')
passwordEntry.bind('<FocusIn>', password_enter)
frame2 = Frame(LogIn, width=160, height=2, bg='black')
frame2.place(x=83, y=310)

#Eye icon - Open/Close
openEye = tk.PhotoImage(file='img/eyeOpen.png')
eyeButton = Button(LogIn, image=openEye, bd=0, bg='white', activebackground='white',
                   cursor='hand2', command=hide)
eyeButton.pack()
eyeButton.place(x=209, y=279)



#Login Button
loginButton = Button(LogIn, text='Přihlášení', font=('Open Sans', 10, 'bold'),
                     fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                     , bd=1, width=9, command=login_user)
loginButton.pack()
loginButton.place(x=120, y=355)

LogIn.mainloop()