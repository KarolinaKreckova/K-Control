from tkinter import *
import tkinter as tk
from tkinter import messagebox

import pymysql


def hide_ikona():
    pridatZam_ikona.config(bg='#c3c3c3')
    stavSkladu_ikona.config(bg='#c3c3c3')

# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()
# --------------------------------------------------------------------------------------------
def pridatZam(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(HlavniStrana, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=250, y=0)

    def clear():
        UsernameAddEntry.delete(0, END)
        PasswordAddEntry.delete(0, END)
        PasswordConfirmEntry.delete(0, END)
        check.set(0)

    # pripojeni do databaze a kontrola
    def connect_database():
        if UsernameAddEntry.get() == '' or PasswordAddEntry.get() == '' or PasswordConfirmEntry.get() == '':
            messagebox.showerror('Error', 'Vyplňte všechna pole')
        elif PasswordAddEntry.get() != PasswordConfirmEntry.get():
            messagebox.showerror('Error', 'Hesla se neshodují')
        elif check.get() == 0:
            messagebox.showerror('Error', 'Zaškrtněte podmínky')
        else:
            try:
                conn = pymysql.connect(host='localhost', user='root')
                mycursor = conn.cursor()
            except:
                messagebox.showerror('Error', 'Nelze se připojit k databázi')
                return
            try:
                query = 'create database uzivatelskadata'
                mycursor.execute(query)
                query = 'use uzivatelskadata'
                mycursor.execute(query)
                query = 'create table if not exist uzivatel(id int auto_increment primary key not null, username varchar (50), ' \
                        'password varchar(40), role varchar(45))'
                mycursor.execute(query)
            except:
                mycursor.execute('use uzivatelskaData')

            query = 'select * from uzivatel where username=%s'
            mycursor.execute(query, (UsernameAddEntry.get()))
            row = mycursor.fetchone()
            if row != None:
                messagebox.showerror('Error', 'Uživatel již existuje')
            else:
                query = 'insert into uzivatel(username, password) values (%s,%s)'
                mycursor.execute(query, (UsernameAddEntry.get(), PasswordAddEntry.get()))

                conn.commit()
                conn.close()
                messagebox.showinfo('Success', 'Přidání uživatele proběhlo v pořádku')
                clear()


    frame = Frame(main_frame, bg='white',padx=30, pady=30, borderwidth=2)
    frame.place(relx=0.5, rely=0.5, anchor='center')
    frame.config(highlightbackground = "black", highlightcolor= "black",
                 highlightthickness=2)



    headingAdd = Label(frame, text='Přidání Zaměstnance',
                       font=('Microsoft Yahei UI Light', 12, 'bold'),
                       bg='white', fg='black')
    headingAdd.grid(row=0, column=0, padx=10, pady=10)

    # Přihlašovací jméno
    UsernameAddLabel = Label(frame, text='Přihlašovací jméno', font=('Microsoft Yahei UI Light', 8, 'bold'),
                             bg='white', fg='black')
    UsernameAddLabel.grid(row=1, column=0,
                          sticky='w', padx=14)
    UsernameAddEntry = Entry(frame, width=25,
                             font=('Microsoft Yahei UI Light', 8, 'bold'), fg='black', bg='light grey')
    UsernameAddEntry.grid(row=2, column=0, sticky='w',
                          padx=14)

    # Heslo
    PasswordAddLabel = Label(frame, text='Heslo', font=('Microsoft Yahei UI Light', 8, 'bold'),
                             bg='white', fg='black')
    PasswordAddLabel.grid(row=3, column=0, sticky='w', padx=14)
    PasswordAddEntry = Entry(frame, width=25, font=('Microsoft Yahei UI Light', 8, 'bold'), fg='black', bg='light grey',
                             show='*')
    PasswordAddEntry.grid(row=4, column=0, sticky='w', padx=14)

    # Kontrola hesla
    PasswordConfirmLabel = Label(frame, text='Kontrola hesla', font=('Microsoft Yahei UI Light', 8, 'bold'),
                                 bg='white', fg='black')
    PasswordConfirmLabel.grid(row=5, column=0, sticky='w', padx=14)
    PasswordConfirmEntry = Entry(frame, width=25, font=('Microsoft Yahei UI Light', 8, 'bold'), fg='black',
                                 bg='light grey', show='*')
    PasswordConfirmEntry.grid(row=6, column=0, sticky='w', padx=14)

    # Doplnek pro mezeru
    TextDoplneni = Label(frame, text='Doplneni pro mezeru', font=('Microsoft Yahei UI Light', 10, 'bold'),
                         bg='white', fg='white')
    TextDoplneni.grid(row=9)

    # Podminky
    check = IntVar()
    Podminky = Checkbutton(frame, text='Zaměstnanec souhlasil s podmínkami',
                           font=('Microsoft Yahei UI Light', 7, 'bold'),
                           bg='white', activebackground='white', cursor='hand2', variable=check)
    Podminky.grid(row=8, column=0)

    # Add Button
    PridaniButton = Button(frame, text='Přidat', font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, bg='light grey',
                           fg='black',
                           activebackground='white', width=17, command=connect_database)
    PridaniButton.grid(row=10)

# --------------------------------------------------------------------------------------------
def kontrolaSkladu(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(HlavniStrana, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.place(x=250, y=0)
    main_frame.configure(height=500, width=500)
    
    def vse():
        main_frame = tk.Frame(HlavniStrana, highlightbackground='black', highlightthickness=2)
        main_frame.pack(side=tk.RIGHT)
        main_frame.pack_propagate(False)
        main_frame.place(x=300, y=350)
        main_frame.configure(height=500, width=500)
        header_bg_color = '#8ac6d1'
        header_fg_color = 'white'
        row_bg_color_1 = '#f0f0f0'
        row_bg_color_2 = 'white'
        conn = pymysql.connect(host='localhost', user='root', database='uzivatelskadata')
        mycursor = conn.cursor()
        query = 'use uzivatelskadata'
        mycursor.execute(query)
        query = 'select * from zbozi_sklad'
        mycursor.execute(query)
        i = 1
        for vse in mycursor:
            for j in range(len(vse)):
                if i % 2 == 0:
                    row_bg_color = row_bg_color_1
                else:
                    row_bg_color = row_bg_color_2
                if i == 0:
                    label_fg_color = header_fg_color
                    label_bg_color = header_bg_color
                else:
                    label_fg_color = 'black'
                    label_bg_color = row_bg_color

                e = Label(main_frame, width=8, text='Id', borderwidth=5, relief='ridge', anchor='w', bg=label_bg_color,
                          fg=label_fg_color)
                e.grid(row=0, column=0)
                e = Label(main_frame, width=8, text='Cislo', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=1)
                e = Label(main_frame, width=8, text='Nazev', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=2)
                e = Label(main_frame, width=8, text='Kod', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=3)
                e = Label(main_frame, width=8, text='Počet', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=4)
                e = Label(main_frame, width=8, text='Cena', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=5)
                e = Label(main_frame, width=8, fg='black', borderwidth=3, relief='ridge', anchor="w", text=vse[j],
                          bg=row_bg_color)
                e.grid(row=i, column=j)
            i += 1
        frame1 = Frame(main_frame, bg='white')
        frame1.place(x=200, y=300)

    def search_zaznam_sklad():
        main_frame = tk.Frame(HlavniStrana, highlightthickness=2)
        main_frame.pack_propagate(False)
        main_frame.pack(side=tk.RIGHT)
        main_frame.place(x=250, y=90)
        main_frame.configure(width=495, height=250)

        conn = pymysql.connect(host='localhost', user='root')
        cursor = conn.cursor()
        query = 'use uzivatelskadata'
        cursor.execute(query)
        result = cursor.fetchall()


        if search_text_var.get() == '':
            messagebox.showerror('Error', 'Vyplňte všechna pole')
        else:
            try:
                conn = pymysql.connect(host='localhost', user='root', database='uzivatelskadata')
                cursor = conn.cursor()
            except:
                messagebox.showerror('Error', 'Připojení se nezdařilo')
                return
            query = 'use uzivatelskadata'
            cursor.execute(query)
            query = "SELECT * FROM zbozi_sklad WHERE nazev=%s"

            vals = (search_text_var.get())
            cursor.execute(query, vals)
            myRows = cursor.fetchall()
            totalRows = cursor.rowcount

            if myRows == None:
                messagebox.showerror('Error', 'Chybný název zboží')

            else:
                main_frame = tk.Frame(HlavniStrana, highlightbackground='black', highlightthickness=2)
                main_frame.pack_propagate(False)
                main_frame.place(x=250, y=120)
                header_bg_color = '#8ac6d1'
                header_fg_color = 'white'
                row_bg_color_1 = '#f0f0f0'
                row_bg_color_2 = 'white'
                i = 1

                for zbozi in myRows:
                    for j in range(len(zbozi)):
                        if i % 2 == 0:
                            row_bg_color = row_bg_color_1
                        else:
                            row_bg_color = row_bg_color_2

                        if i == 0:
                            label_fg_color = header_fg_color
                            label_bg_color = header_bg_color
                        else:
                            label_fg_color = 'black'
                            label_bg_color = row_bg_color

                        e = Label(main_frame, width=10, text='Id', borderwidth=5, relief='ridge', anchor='w', bg=label_bg_color,
                                  fg=label_fg_color)
                        e.grid(row=0, column=0)
                        e = Label(main_frame, width=10, text='Číslo', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=1)
                        e = Label(main_frame, width=10, text='Název', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=2)
                        e = Label(main_frame, width=10, text='Kód', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=3)
                        e = Label(main_frame, width=10, text='Počet', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=4)
                        e = Label(main_frame, width=10, text='Cena', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=5)
                        e = Label(main_frame, width=10, fg='black', borderwidth=3, relief='ridge', anchor="w", text=zbozi[j],
                                  bg=row_bg_color)
                        e.grid(row=i, column=j)
                    i += 1

    messageLabel = Label(main_frame, text='Zadejte název požadovaného zboží', bg='light grey')
    messageLabel.place(x=138, y=10, height=35)
    messageLabel.place(x=138, y=10, height=35)
    search_text_var = tk.StringVar()
    Zbozi = tk.Entry(main_frame,textvariable=search_text_var)
    buttonSearch = tk.Button(main_frame,text="Search", command=search_zaznam_sklad)
    Zbozi.pack(side='left', padx=5, pady=5)
    buttonSearch.pack(side='left', padx=5, pady=5)
    Zbozi.place(x=150, y=70)
    buttonSearch.place(x=280, y=65)

    VseButton = tk.Button(main_frame,text="Zobrazit Vše", command=vse)
    VseButton.pack(side='left', padx=5, pady=5)
    VseButton.place(x=360, y=65)



# --------------------------------------------------------------------------------------------

HlavniStrana = tk.Tk()
HlavniStrana.title('Hlavní strana')
HlavniStrana.resizable(False, False)
options_frame = tk.Frame(HlavniStrana, bg='#c3c3c3')
options_frame.pack(side=tk.RIGHT)
options_frame.pack_propagate(False)
window_width = 750
window_height = 500
screen_width = HlavniStrana.winfo_screenwidth()
screen_height = HlavniStrana.winfo_screenheight()

x_axis = (screen_width / 2) - (window_width / 2)
y_axis = (screen_height / 2) - (window_height / 2)

HlavniStrana.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_axis), int(y_axis)))

#Zjištění velikosti monitoru pro centrování
#print(screen_width)
#print(screen_height)

main_frame = tk.Frame(HlavniStrana, highlightbackground='black', highlightthickness=2)
main_frame.pack(side=tk.RIGHT)
main_frame.pack_propagate(False)
main_frame.configure(height=500, width=500)

def LogOut():
    HlavniStrana.destroy()
# --------------------------------------------------------------------------------------------
#Button k Přidání zaměstnance
pridatZamButton = Button(HlavniStrana, text='Přidání zaměstnance', font=('Open Sans', 13, 'bold'),
                     fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                     ,bd=1, width=19, command=lambda: ikona(pridatZam_ikona, pridatZam(main_frame)))
pridatZamButton.pack()
pridatZamButton.place(x=30, y=190)

pridatZam_ikona = Label(HlavniStrana, text ='', bg='#c3c3c3')
pridatZam_ikona.place(x=25, y=189, height=35)






# --------------------------------------------------------------------------------------------
# button pro kontrolu skladu
stavSkladuButton = Button(HlavniStrana, text='Kontrola skladu', font=('Open Sans', 13, 'bold'),
                          fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                          , bd=1, width=19, command=lambda: ikona(stavSkladu_ikona, kontrolaSkladu(main_frame) ))

stavSkladuButton.pack()
stavSkladuButton.place(x=30, y=310)

stavSkladu_ikona = Label(HlavniStrana, text='', bg='#c3c3c3')
stavSkladu_ikona.place(x=25, y=309, height=35)

# --------------------------------------------------------------------------------------------
LogOut = Button(HlavniStrana, text="Odhlásit se",font=('Open Sans', 8, 'bold'),
                              fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                              , width=10,command=LogOut)
LogOut.pack()
LogOut.place(x=150,y=10)
