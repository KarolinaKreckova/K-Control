
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
import ObjednavkaStranajedna
import ObjednavkaStranaDva
import pymysql



def hide_ikona():
    stavSkladu_ikona.config(bg='#c3c3c3')
    email_ikona.config(bg='#c3c3c3')
    ObjednavkaStranajedna.objednavka_ikona.config(bg='#c3c3c3')
    ObjednavkaStranaDva.poznamky_ikona.config(bg='#c3c3c3')
    ObjednavkaStranaDva.zaloha_ikona.config(bg='#c3c3c3')
    ObjednavkaStranaDva.email_ikona.config(bg='#c3c3c3')

# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()

# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()
# --------------------------------------------------------------------------------------------

def Email(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=250, y=0)
    messageLabel = Label(ObjednavkaStranajedna.Objednavka, text='Email', bg='light grey', font=(40))
    messageLabel.place(x=470, y=10, height=40)
    def clear():
        OdesilatelAddEntry.delete(0, END)
        KomuAddEntry.delete(0, END)
        PredmetAddEntry.delete(0, END)
        ObsahAddEntry.delete(0, END)
        PoznamkaAddEntry.delete(0, END)
        NutnostAddEntry.delete(0, END)
        check.set(0)

    # pripojeni do databaze a kontrola
    def connect_database():
        if OdesilatelAddEntry.get() == '' or KomuAddEntry.get() == '' or PredmetAddEntry.get() == ''\
                or ObsahAddEntry.get() == '':
            messagebox.showerror('Error', 'Vyplňte všechna pole')
        else:
            try:
                conn = pymysql.connect(host='localhost', user='root')
                mycursor = conn.cursor()
            except:
                messagebox.showerror('Error', 'Nelze se připojit k databázi')
                return
            try:
                query = 'create database uzivatelskaData'
                mycursor.execute(query)
                query = 'use uzivatelskaData'
                mycursor.execute(query)
                query = 'create table if not exist email(id int auto_increment primary key not null, odesilatel varchar (50), ' \
                        'komu varchar(50), predmet varchar(50), obsah varchar(50), poznamka varchar(50), nutnost varchar(10))'
                mycursor.execute(query)
            except:
                mycursor.execute('use uzivatelskaData')


            query = 'insert into email(odesilatel,komu, predmet, obsah, poznamka, nutnost) values (%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query, (OdesilatelAddEntry.get(), KomuAddEntry.get(),PredmetAddEntry.get(),ObsahAddEntry.get(),
                                     PoznamkaAddEntry.get(), NutnostAddEntry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Záloha emailu proběhla v pořádku')
            clear()

    frame = Frame(main_frame, bg='white',padx=30, pady=30, borderwidth=2)
    frame.place(relx=0.5, rely=0.55, anchor='center', width=450, height=410)
    frame.config(highlightbackground = "black", highlightcolor= "black", highlightthickness=2)


    # Odesilatel
    OdesilatelAddLabel = Label(frame, text='Odesílatel', font=( 8),
                             bg='white', fg='black')
    OdesilatelAddLabel.place(x=10, y=10)
    OdesilatelAddEntry = Entry(frame, width=20, font=( 8), fg='black', bg='light grey')
    OdesilatelAddEntry.place(x=10, y=30)

    # Komu
    KomuAddLabel = Label(frame, text='Komu', font=( 8),
                             bg='white', fg='black')
    KomuAddLabel.place(x=10, y=60)
    KomuAddEntry = Entry(frame, width=20, font=( 8), fg='black', bg='light grey',
                        )
    KomuAddEntry.place(x=10, y=80)

    # Predmet
    PredmetAddLabel = Label(frame, text='Předmět', font=( 8),
                                 bg='white', fg='black')
    PredmetAddLabel.place(x=10, y=110)
    PredmetAddEntry = Entry(frame, width=30, font=( 8), fg='black',
                                 bg='light grey')
    PredmetAddEntry.place(x=10, y=130)


    # Obsah
    ObsahAddLabel = Label(frame, text='Obsah', font=( 8),
                            bg='white', fg='black')
    ObsahAddLabel.place(x=10, y=160)
    ObsahAddEntry = Entry(frame, width=40, font=( 8),
                         fg='black', bg='light grey')
    ObsahAddEntry.place(x=10, y=180)

    # poznamka
    PoznamkaAddLabel = Label(frame, text='Poznámka', font=(8),
                          bg='white', fg='black')
    PoznamkaAddLabel.place(x=10, y=210)
    PoznamkaAddEntry = Entry(frame, width=40, font=(8),
                          fg='black', bg='light grey')
    PoznamkaAddEntry.place(x=10, y=230)

    # nutnost
    NutnostAddLabel = Label(frame, text='Nutnost', font=( 8),
                            bg='white', fg='black')
    NutnostAddLabel.place(x=10, y=260)
    NutnostAddEntry = Entry(frame, width=40, font=( 8),
                         fg='black', bg='light grey')
    NutnostAddEntry.place(x=10, y=280)

    # Podminky
    check = IntVar()
    Podminky = Checkbutton(frame, text='Potvrdit přečtení',
                           font=(5),
                           bg='white', activebackground='white', cursor='hand2', variable=check)
    Podminky.place(x=10, y=330)

    # Odeslat Button
    SendButton = Button(frame, text='Odeslat', font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, bg='light grey',
                           fg='black',
                           activebackground='white', width=17, command=connect_database)
    SendButton.place(x=200, y=330)

# --------------------------------------------------------------------------------------------
def kontrolaSkladu(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.place(x=250, y=0)
    main_frame.configure(height=500, width=500)
    def vse():
        main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightbackground='black', highlightthickness=2)
        main_frame.pack(side=tk.RIGHT)
        main_frame.pack_propagate(False)
        main_frame.place(x=250, y=350)
        main_frame.configure(height=500, width=500)
        header_bg_color = '#8ac6d1'
        header_fg_color = 'white'
        row_bg_color_1 = '#f0f0f0'
        row_bg_color_2 = 'white'
        conn = pymysql.connect(host='localhost', user='root')
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

                e = Label(main_frame, width=10, text='Id', borderwidth=5, relief='ridge', anchor='w', bg=label_bg_color,
                          fg=label_fg_color)
                e.grid(row=0, column=0)
                e = Label(main_frame, width=10, text='Cislo', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=1)
                e = Label(main_frame, width=10, text='Nazev', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=2)
                e = Label(main_frame, width=10, text='Kod', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=3)
                e = Label(main_frame, width=10, text='Počet', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=4)
                e = Label(main_frame, width=10, text='Cena', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=5)
                e = Label(main_frame, width=10, fg='black', borderwidth=3, relief='ridge', anchor="w", text=vse[j],
                          bg=row_bg_color)
                e.grid(row=i, column=j)
            i += 1
        frame1 = Frame(main_frame, bg='white')
        frame1.place(x=200, y=300)

    def search_zaznam_sklad():
        main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightthickness=2)
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
                conn = pymysql.connect(host='localhost', user='root')
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
                main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightbackground='black', highlightthickness=2)
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
    messageLabel.place(x=140, y=10, height=37)
    search_text_var = tk.StringVar()
    Zbozi = tk.Entry(main_frame, textvariable=search_text_var)
    buttonSearch = tk.Button(main_frame, text="Search", command=search_zaznam_sklad)
    Zbozi.pack(side='left', padx=5, pady=5)
    buttonSearch.pack(side='left', padx=5, pady=5)
    Zbozi.place(x=150, y=70)
    buttonSearch.place(x=280, y=65)
    VseButton = tk.Button(main_frame,text="Zobrazit Vše", command=vse)
    VseButton.pack(side='left', padx=5, pady=5)
    VseButton.place(x=360, y=65)
    VseButton = tk.Button(main_frame, text="Zobrazit Vše", command=vse)
    VseButton.pack(side='left', padx=5, pady=5)
    VseButton.place(x=360, y=65)
# --------------------------------------------------------------------------------------------

# button pro kontrolu skladu
stavSkladuButton = Button(ObjednavkaStranajedna.Objednavka, text='Kontrola skladu', font=('Open Sans', 13, 'bold'),
                          fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                          , bd=1, width=19, command=lambda: ikona(stavSkladu_ikona, kontrolaSkladu(ObjednavkaStranajedna.main_frame) ))

stavSkladuButton.pack()
stavSkladuButton.place(x=30, y=330)

stavSkladu_ikona = Label(ObjednavkaStranajedna.Objednavka, text='', bg='#c3c3c3')
stavSkladu_ikona.place(x=25, y=329, height=35)
# --------------------------------------------------------------------------------------------
#button pro email
emailButton = Button(ObjednavkaStranajedna.Objednavka, text='Email', font=('Open Sans', 13, 'bold'),
                     fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                     ,bd=1, width=19, command=lambda: ikona(email_ikona, Email(ObjednavkaStranajedna.main_frame)))
emailButton.pack()
emailButton.place(x=30, y=160)

email_ikona = Label(ObjednavkaStranajedna.Objednavka, text ='', bg='#c3c3c3')
email_ikona.place(x=25, y=159, height=35)

ObjednavkaStranajedna.mainloop()