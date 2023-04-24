import json
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk

import pymysql


def hide_ikona():
    stavobjednavky_ikona.config(bg='#c3c3c3')
    email_ikona.config(bg='#c3c3c3')
# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()

# --------------------------------------------------------------------------------------------


def stavObjednavky(ctverec):
    def otevritObjednavky():
        otevrit = tk.Tk()
        otevrit.title('Objednávky')
        otevrit.resizable(False, False)
        window_width = 465
        window_height = 300
        screen_width = Kontrola.winfo_screenwidth()
        screen_height = Kontrola.winfo_screenheight()

        x_axis = (screen_width / 2) - (window_width / 2)
        y_axis = (screen_height / 2) - (window_height / 2)

        otevrit.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_axis), int(y_axis)))

        # Zjištění velikosti monitoru pro centrování
        # print(screen_width)
        # print(screen_height)



        header_bg_color = '#8ac6d1'
        header_fg_color = 'white'
        row_bg_color_1 = '#f0f0f0'
        row_bg_color_2 = 'white'

        conn = pymysql.connect(host='localhost', user='root')
        mycursor = conn.cursor()
        query = 'use objednavka'
        mycursor.execute(query)

        query = 'SELECT faktura.jmeno, faktura.prijmeni, faktura.telefon ,zbozi.popis, zbozi.pocet,zbozi.cena, (zbozi.pocet * zbozi.cena) AS cena\
                FROM faktura INNER JOIN zbozi ON faktura.zbozi_id = zbozi.id \
                '
        mycursor.execute(query)
        FrameZbozi = Frame(otevrit, bg='white')
        FrameZbozi.place(x=100, y=50, anchor='center')
        FrameZbozi.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)

        i = 1
        for objednavka in mycursor:
            for j in range(len(objednavka)):
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

                    e = Label(otevrit, width=8, text='Jméno', borderwidth=4, relief='ridge', anchor='center',
                              bg=label_bg_color,
                              fg=label_fg_color)
                    e.grid(row=0, column=0)
                    e = Label(otevrit, width=8, text='Příjmení', borderwidth=4, relief='ridge', anchor='center',
                              bg=label_bg_color, fg=label_fg_color)
                    e.grid(row=0, column=1)
                    e = Label(otevrit, width=8, text='Telefon', borderwidth=4, relief='ridge', anchor='center',
                              bg=label_bg_color, fg=label_fg_color)
                    e.grid(row=0, column=2)
                    e = Label(otevrit, width=8, text='Popis', borderwidth=4, relief='ridge', anchor='center',
                              bg=label_bg_color, fg=label_fg_color)
                    e.grid(row=0, column=3)
                    e = Label(otevrit, width=8, text='Počet', borderwidth=4, relief='ridge', anchor='center',
                              bg=label_bg_color, fg=label_fg_color)
                    e.grid(row=0, column=4)
                    e = Label(otevrit, width=8, text='Cena / ks', borderwidth=4, relief='ridge', anchor='center',
                              bg=label_bg_color, fg=label_fg_color)
                    e.grid(row=0, column=5)
                    e = Label(otevrit, width=8, text='Cena', borderwidth=4, relief='ridge', anchor='center',
                              bg=label_bg_color, fg=label_fg_color)
                    e.grid(row=0, column=6)
                    e = Label(otevrit, width=8, fg='black', borderwidth=4, relief='ridge', anchor="center",
                              text=objednavka[j],
                              bg=row_bg_color)
                    e.grid(row=i, column=j)

            i += 1

    main_frame = tk.Frame(Kontrola, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=150, y=0)


    header_bg_color = '#8ac6d1'
    header_fg_color = 'white'
    row_bg_color_1 = '#f0f0f0'
    row_bg_color_2 = 'white'

    conn = pymysql.connect(host='localhost', user='root')
    mycursor = conn.cursor()
    query = 'use objednavka'
    mycursor.execute(query)


    query ='SELECT faktura.jmeno, faktura.prijmeni, faktura.telefon ,zbozi.popis, zbozi.pocet,zbozi.cena, (zbozi.pocet * zbozi.cena) AS cena\
        FROM faktura INNER JOIN zbozi ON faktura.zbozi_id = zbozi.id \
        '
    mycursor.execute(query)
    main_frame.place(x=250, y=0)

    def delete(row):
        my_var = messagebox.askyesnocancel("Smazání", "Opravdu chcete tento záznam smazat?", icon="warning",
                                           default="no")
        if my_var:
            # Delete row from database
            r_set = 'DELETE FROM faktura WHERE telefon=%s'
            mycursor.execute(r_set, row[2])
            conn.commit()

        # Remove widgets from the main_frame
            for j in range(len(row)):
                e = Label(main_frame, width=8, fg='black', borderwidth=4, relief='ridge', anchor="center", text='x',
                          bg=row_bg_color)
                e.grid(row=i, column=1)
            messagebox.showerror("Smazání", "Smazání záznamu proběhlo v pořádku")


    def refresh_table():
        for widget in main_frame.winfo_children():
            widget.destroy()

            # Recreate the table with updated data from the database
        query = 'SELECT faktura.jmeno, faktura.prijmeni, faktura.telefon ,zbozi.popis, zbozi.pocet,zbozi.cena, (zbozi.pocet * zbozi.cena) AS cena FROM faktura INNER JOIN zbozi ON faktura.zbozi_id = zbozi.id'
        mycursor.execute(query)
    refresh_table()
    FrameZbozi = Frame(Kontrola, bg='white')
    FrameZbozi.place(x=500, y=200, anchor='center')
    FrameZbozi.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)

    i = 1
    for objednavka in mycursor:
        for j in range(len(objednavka)):
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


                e = Label(FrameZbozi,width=8, text='Jméno', borderwidth=4, relief='ridge', anchor='center', bg=label_bg_color,
                          fg=label_fg_color)
                e.grid(row=0, column=0)
                e = Label(FrameZbozi, width=8, text='Příjmení', borderwidth=4, relief='ridge', anchor='center',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=1)
                e = Label(FrameZbozi, width=8, text='Telefon', borderwidth=4, relief='ridge', anchor='center',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=2)
                e = Label(FrameZbozi, width=8, text='Popis', borderwidth=4, relief='ridge', anchor='center',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=3)
                e = Label(FrameZbozi, width=8, text='Počet', borderwidth=4, relief='ridge', anchor='center',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=4)
                e = Label(FrameZbozi, width=8, text='Cena / ks', borderwidth=4, relief='ridge', anchor='center',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=5)
                e = Label(FrameZbozi, width=8, text='Cena', borderwidth=4, relief='ridge', anchor='center',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=6)
                e = Label(FrameZbozi, width=8, fg='black', borderwidth=4, relief='ridge', anchor="center", text=objednavka[j],
                          bg=row_bg_color)
                e.grid(row=i, column=j)
                e = Button(FrameZbozi, text="X", command=lambda row = objednavka: delete(row))
                e.grid(row=i, column=j+1)
        i +=1

    refreshframe = Frame(Kontrola, bg='white')
    refreshframe.place(x=680,y=350, anchor='center')
    refreshframe.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)

    refresh_button = tk.Button(refreshframe, text="Refresh", font=("Arial", 12), bg="white", fg="black",
                               command=lambda :stavObjednavky(Kontrola))
    refresh_button.grid(pady=10, padx=10)

    messageLabel = Label(Kontrola, text='Mazání záznamů', bg='light grey')
    messageLabel.place(x=450, y=10, height=35)

    buttonSearch = tk.Button(main_frame, text="Otevřít objednávky v novém okně", command=otevritObjednavky)
    buttonSearch.pack(side='left', padx=5, pady=5)
    buttonSearch.place(x=300, y=400)

# --------------------------------------------------------------------------------------------


def Email(ctverec):

    ctverec.tkraise()
    main_frame = tk.Frame(Kontrola, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=250, y=0)
    messageLabel = Label(Kontrola, text='Email', bg='light grey', font=(40))
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

def LogOut():
    Kontrola.destroy()

# --------------------------------------------------------------------------------------------

Kontrola = Tk()
Kontrola.title('Hlavní strana')
Kontrola.resizable(False, False)
options_frame = tk.Frame(Kontrola, bg='#c3c3c3')
options_frame.pack(side=tk.RIGHT)
options_frame.pack_propagate(False)
window_width = 750
window_height = 500
screen_width = Kontrola.winfo_screenwidth()
screen_height = Kontrola.winfo_screenheight()

x_axis = (screen_width / 2) - (window_width / 2)
y_axis = (screen_height / 2) - (window_height / 2)

Kontrola.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_axis), int(y_axis)))

#Zjištění velikosti monitoru pro centrování
#print(screen_width)
#print(screen_height)

main_frame = tk.Frame(Kontrola, highlightbackground='black', highlightthickness=2)
main_frame.pack(side=tk.RIGHT)
main_frame.pack_propagate(False)
main_frame.configure(height=500, width=500)


# --------------------------------------------------------------------------------------------
LogOut = Button(Kontrola, text="Odhlásit se",font=('Open Sans', 8, 'bold'),
                              fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                              , width=10,command=LogOut)
LogOut.pack()
LogOut.place(x=150,y=10)

# --------------------------------------------------------------------------------------------
# button pro kontrolu poslanych objednavek
stavObjednavkyButton = Button(Kontrola, text='Stav objednávky', font=('Open Sans', 13, 'bold'),
                              fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                              , width=19, command=lambda: ikona(stavobjednavky_ikona,stavObjednavky(main_frame)))

stavObjednavkyButton.pack()
stavObjednavkyButton.place(x=30, y=330)

stavobjednavky_ikona = Label(Kontrola, text='', bg='#c3c3c3')
stavobjednavky_ikona.place(x=25, y=329, height=35)
# --------------------------------------------------------------------------------------------


#button pro email
emailButton = Button(Kontrola, text='Email', font=('Open Sans', 13, 'bold'),
                     fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                     ,bd=1, width=19, command=lambda: ikona(email_ikona, Email(main_frame)))
emailButton.pack()
emailButton.place(x=30, y=70)

email_ikona = Label(Kontrola, text ='', bg='#c3c3c3')
email_ikona.place(x=25, y=69, height=35)