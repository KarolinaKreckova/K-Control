import json
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
import kontrolorStranajedna
import pymysql


def hide_ikona():
    kontrolorStranajedna.email_ikona.config(bg='#c3c3c3')
    kontrolorStranajedna.stavobjednavky_ikona.config(bg='#c3c3c3')
    stavSkladu_ikona.config(bg='#c3c3c3')

# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()
# --------------------------------------------------------------------------------------------
def kontrolaSkladu(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(kontrolorStranajedna.Kontrola, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.place(x=250, y=208)
    invoice_list = []

    def add_item():
        try:
            cislo = int(cisloEntry.get())
            nazev = nazevEntry.get()
            kod = kodEntry.get()
            pocet= int(pocetSpin.get())
            cena = cenaSpin.get()
            items = [cislo, nazev, kod, pocet, cena]
            clear_item()
            invoice_list.append(items)
        except ValueError:
            error_label.config(text="Chyba")

    def delete(row):
        my_var = messagebox.askyesnocancel("Smazání", "Opravdu chcete tento záznam smazat?", icon="warning",
                                           default="no")
        if my_var:
            # Delete row from database
            r_set = 'DELETE FROM zbozi_sklad where nazev =%s'
            mycursor.execute(r_set,row[1])
            conn.commit()

            # Remove widgets from the main_frame
            for j in range(len(row)):
                e = Label(main_frame, width=8, fg='black', borderwidth=4, relief='ridge', anchor="center", text='x',
                          bg=row_bg_color)
                e.grid(row=i, column=1)
            messagebox.showerror("Smazání", "Smazání záznamu proběhlo v pořádku")

    def refresh_table():
        main_frame = tk.Frame(kontrolorStranajedna.Kontrola, highlightbackground='black', highlightthickness=2)
        main_frame.pack(side=tk.RIGHT)
        main_frame.pack_propagate(False)
        main_frame.place(x=250, y=208)
        for widget in main_frame.winfo_children():
            widget.destroy()

            # Recreate the table with updated data from the database
        query = 'SELECT * from zbozi_sklad'
        mycursor.execute(query)


    def clear_item():
        cisloEntry.delete(0, tk.END)
        nazevEntry.delete(0, tk.END)
        kodEntry.delete(0, tk.END)
        pocetSpin.delete(0, tk.END)
        pocetSpin.insert(0, "1")
        cenaSpin.delete(0, tk.END)
        cenaSpin.insert(0, "0")

    def connect_database():
        global i
        # kontrola, zda jsou všechna pole vyplněna
        if cisloEntry.get() == '' or nazevEntry.get() == '' \
        or kodEntry.get() == '' or pocetSpin.get() == ''or cenaSpin.get() == '' :
            messagebox.showerror('Error', 'Vyplňte všechna pole')

        else:
            try:
                # připojení k databázi
                conn = pymysql.connect(host='localhost', user='root', password='', database='uzivatelskadata')
                mycursor = conn.cursor()
            except ValueError:
                messagebox.showerror("Chyba")

            # vytvoření tabulek, pokud neexistují
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS zbozi_sklad (id INT AUTO_INCREMENT PRIMARY KEY, cislo INT, nazev VARCHAR(50),'
                'kod varchar(50), pocet int, cena int)')

            try:
                cislo = int(cisloEntry.get())
                nazev = nazevEntry.get()
                # vložení dat do tabulky zbozi
                queryPrvni = 'INSERT INTO zbozi_sklad (cislo, nazev, kod, pocet, cena) VALUES (%s, %s, %s,%s,%s)'
                mycursor.execute(queryPrvni, (cisloEntry.get(), nazevEntry.get(), kodEntry.get(), pocetSpin.get(), cenaSpin.get()))
                id = mycursor.lastrowid  # získání ID posledně vloženého záznamu

                conn.commit()  # potvrzení změn v databázi
                conn.close()  # ukončení spojení s databází
                messagebox.showinfo('Success', 'Přidání položek proběhlo v pořádku')
                clear_item()
            except ValueError:
                messagebox.showerror("chyba", "Byla zadána špatná hodnota")
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
    error_label = Label(kontrolorStranajedna.main_frame, fg="red")
    error_label.pack()
    refresh_table()



    i = 1
    for zbozi in mycursor:
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

            e = Label(main_frame, width=10, text='Id', borderwidth=3, relief='ridge', anchor='w', bg=label_bg_color,
                      fg=label_fg_color)
            e.grid(row=0, column=0)
            e = Label(main_frame, width=10, text='Číslo', borderwidth=3, relief='ridge', anchor='w',
                      bg=label_bg_color, fg=label_fg_color)
            e.grid(row=0, column=1)
            e = Label(main_frame, width=10, text='Název', borderwidth=3, relief='ridge', anchor='w',
                      bg=label_bg_color, fg=label_fg_color)
            e.grid(row=0, column=2)
            e = Label(main_frame, width=10, text='Kód', borderwidth=3, relief='ridge', anchor='w',
                      bg=label_bg_color, fg=label_fg_color)
            e.grid(row=0, column=3)
            e = Label(main_frame, width=10, text='Pocet', borderwidth=3, relief='ridge', anchor='w',
                      bg=label_bg_color, fg=label_fg_color)
            e.grid(row=0, column=4)
            e = Label(main_frame, width=10, text='Cena', borderwidth=3, relief='ridge', anchor='w',
                      bg=label_bg_color, fg=label_fg_color)
            e.grid(row=0, column=5)
            e = Label(main_frame, width=10, fg='black', borderwidth=3, relief='ridge', anchor="w", text=zbozi[j],
                      bg=row_bg_color)
            e.grid(row=i, column=j)
            e = Button(main_frame, text="X", command=lambda row=zbozi: delete(row))
            e.grid(row=i, column=j + 1)
        i += 1

    refreshframe = Frame(kontrolorStranajedna.Kontrola, bg='white')
    refreshframe.place(x=680, y=460, anchor='center')
    refreshframe.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)
    refresh_button = tk.Button(refreshframe, text="Refresh", font=("Arial", 12), bg="white", fg="black",
                               command=lambda: kontrolaSkladu(kontrolorStranajedna.main_frame))
    refresh_button.grid(pady=10, padx=10)
    cisloLabel = Label(kontrolorStranajedna.main_frame, text="Číslo")
    cisloLabel.grid(row=0, column=0)
    cisloLabel.place(x=55,y=15)
    cisloEntry = Entry(kontrolorStranajedna.main_frame)
    cisloEntry.grid(row=1, column=0)
    cisloEntry.place(x=20, y=35)
    nazev_label = Label(kontrolorStranajedna.main_frame, text="Název")
    nazev_label.grid(row=0, column=1)
    nazev_label.place(x=220,y=15)
    nazevEntry = Entry(kontrolorStranajedna.main_frame)
    nazevEntry.grid(row=1, column=1)
    nazevEntry.place(x=180, y=35)
    kod_label = Label(kontrolorStranajedna.main_frame, text="Kód")
    kod_label.grid(row=0, column=2)
    kod_label.place(x=385, y=15)
    kodEntry = Entry(kontrolorStranajedna.main_frame)
    kodEntry.grid(row=1, column=2)
    kodEntry.place(x=344, y=35)
    pocet_label = Label(kontrolorStranajedna.main_frame, text="Počet kusů")
    pocet_label.grid(row=2, column=0)
    pocet_label.place(x=100,y=70)
    pocetSpin = Spinbox(kontrolorStranajedna.main_frame, from_=1, to=100)
    pocetSpin.grid(row=3, column=0)
    pocetSpin.place(x=70, y=90)
    cena_label = tk.Label(kontrolorStranajedna.main_frame, text="Cena")
    cena_label.grid(row=2, column=2)
    cena_label.place(x=330,y=70)
    cenaSpin = Spinbox(kontrolorStranajedna.main_frame, from_=0, to=100000, increment=10)
    cenaSpin.grid(row=3, column=2)
    cenaSpin.place(x=280, y=90)
    add_item_button = Button(kontrolorStranajedna.main_frame, text="Přidat", command=connect_database, width=10)
    add_item_button.place(x=200, y=140)

# --------------------------------------------------------------------------------------------

# button pro kontrolu skladu
stavSkladuButton = Button(kontrolorStranajedna.Kontrola, text='Sklad', font=('Open Sans', 13, 'bold'),
                          fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                          , bd=1, width=19, command=lambda: ikona(stavSkladu_ikona, kontrolaSkladu(kontrolorStranajedna.main_frame) ))

stavSkladuButton.pack()
stavSkladuButton.place(x=30, y=240)

stavSkladu_ikona = Label(kontrolorStranajedna.Kontrola, text='', bg='#c3c3c3')
stavSkladu_ikona.place(x=25, y=239, height=35)


