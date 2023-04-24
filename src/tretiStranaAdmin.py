import datetime
import os.path
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import pymysql
from docxtpl import DocxTemplate
import prvniStranaAdmin
import druhaStranaAdmin
from tkinter import ttk, messagebox
import json

def hide_ikona():
    objednavka_ikona.config(bg='#c3c3c3')
    stavobjednavky_ikona.config(bg='#c3c3c3')
    druhaStranaAdmin.poznamky_ikona.config(bg='#c3c3c3')
    druhaStranaAdmin.prava_ikona.config(bg='#c3c3c3')

# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()

# --------------------------------------------------------------------------------------------

def objednavka(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(prvniStranaAdmin.HlavniStrana, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=2)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=250, y=0)

    def connect_database():
        global i
        # kontrola, zda jsou všechna pole vyplněna
        if first_name_entry.get() == '' or last_name_entry.get() == '' \
                or pocet_spinBox.get() == '' or popis_entry.get() == '' \
                or phone_entry.get() == '' or cena_spinBox.get() == '':
            messagebox.showerror('Error', 'Vyplňte všechna pole')
        else:
            try:
                # připojení k databázi

                conn = pymysql.connect(host='localhost', user='root', password='', database='Objednavka')
                mycursor = conn.cursor()

            except:
                messagebox.showerror('Error', 'Nelze se připojit k databázi')
                return

            # vytvoření tabulek, pokud neexistují
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS zbozi (id INT AUTO_INCREMENT PRIMARY KEY, pocet INT, popis VARCHAR(100), cena INT)')
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS Faktura (id INT AUTO_INCREMENT PRIMARY KEY, jmeno VARCHAR(50), prijmeni VARCHAR(50), telefon VARCHAR(9), zbozi_id INT, FOREIGN KEY (zbozi_id) REFERENCES zbozi(id))')

            # vložení dat do tabulky zbozi
            queryPrvni = 'INSERT INTO zbozi (pocet, popis, cena) VALUES (%s, %s, %s)'
            mycursor.execute(queryPrvni, (pocet_spinBox.get(), popis_entry.get(), cena_spinBox.get()))
            zbozi_id = mycursor.lastrowid  # získání ID posledně vloženého záznamu

            # vložení dat do tabulky faktura
            query = 'INSERT INTO Faktura (jmeno, prijmeni, telefon, zbozi_id) VALUES (%s, %s, %s, %s)'
            mycursor.execute(query, (first_name_entry.get(), last_name_entry.get(), phone_entry.get(), zbozi_id))

            conn.commit()  # potvrzení změn v databázi
            conn.close()  # ukončení spojení s databází
            messagebox.showinfo('Success', 'Přidání položek proběhlo v pořádku')

    def clear_item():
        pocet_spinBox.delete(0, tk.END)
        pocet_spinBox.insert(0, "1")
        popis_entry.delete(0, tk.END)
        cena_spinBox.delete(0, tk.END)
        cena_spinBox.insert(0, "0")

    invoice_list = []

    def add_item():
        pocetKusu = int(pocet_spinBox.get())
        popis = popis_entry.get()
        cenaKus = float(cena_spinBox.get())
        cena = pocetKusu * cenaKus
        items = [pocetKusu, popis, cenaKus, cena]
        tree.insert('', 0, values=items)
        clear_item()
        invoice_list.append(items)

    def new():
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        clear_item()
        tree.delete(*tree.get_children())
        invoice_list.clear()

    def Faktura():
        global i
        doc = DocxTemplate("Faktura/invoice_template.docx")
        jmeno = first_name_entry.get() + last_name_entry.get()
        telefon = phone_entry.get()
        prepocet = sum(item[3] for item in invoice_list)
        dan = 0.21
        cena = prepocet * (1 - dan)

        doc.render({"jmeno": jmeno,
                    "telefon": telefon,
                    "invoice_list": invoice_list,
                    "prepocet": prepocet,
                    "dan": str(dan * 100) + "%",
                    "total": cena})
        doc_name = "Nova_faktura" + jmeno + \
                   datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S") + ".docx"
        doc.save(doc_name)
        messagebox.showinfo("Faktura", "Vygenerování proběhlo v pořádku")
        new()
    ostatniFrame = Frame(prvniStranaAdmin.HlavniStrana)
    ostatniFrame.pack()
    ostatniFrame.place(x=150, y=200)


    first_name_label = Label(main_frame, text="Jméno")
    first_name_label.grid(row=0, column=0)
    first_name_label.place(x=55,y=15)

    last_name_label = Label(main_frame, text="Příjmení")
    last_name_label.grid(row=0, column=1)
    last_name_label.place(x=220,y=15)


    first_name_entry = Entry(main_frame)
    first_name_entry.grid(row=1, column=0)
    first_name_entry.place(x=20, y=35)

    last_name_entry = Entry(main_frame)
    last_name_entry.grid(row=1, column=1)
    last_name_entry.place(x=180, y=35)

    phone_label = Label(main_frame, text="Telefon")
    phone_label.grid(row=0, column=2)
    phone_label.place(x=385, y=15)

    phone_entry = Entry(main_frame)
    phone_entry.grid(row=1, column=2)
    phone_entry.place(x=344, y=35)

    pocet_label = Label(main_frame, text="Počet kusů")
    pocet_label.grid(row=2, column=0)
    pocet_label.place(x=10,y=70)

    pocet_spinBox = Spinbox(main_frame, from_=1, to=100)
    pocet_spinBox.grid(row=3, column=0)
    pocet_spinBox.place(x=15, y=90)

    popis_label = Label(main_frame, text="Popis")
    popis_label.grid(row=2, column=1)
    popis_label.place(x=220,y=70)

    popis_entry = Entry(main_frame)
    popis_entry.grid(row=3, column=1)
    popis_entry.place(x=180,y=90)

    cena_label = tk.Label(main_frame, text="Cena")
    cena_label.grid(row=2, column=2)
    cena_label.place(x=390,y=70)

    cena_spinBox = Spinbox(main_frame, from_=0, to=100000, increment=10)
    cena_spinBox.grid(row=3, column=2)
    cena_spinBox.place(x=340, y=90)

    add_item_button = Button(main_frame, text="Přidat", command=add_item, width=10)
    add_item_button.place(x=400, y=150)
    save_item_button = Button(main_frame, text="Uložit", command=connect_database, width=10)
    save_item_button.place(x=300, y=150)

    treeFrame = Frame(prvniStranaAdmin.HlavniStrana)
    treeFrame.pack()
    treeFrame.place(x=257, y=200)
    columns = ("Počet", "Popis", "Cena za kus", "Cena")

    tree = ttk.Treeview(treeFrame, columns=columns, show="headings")
    tree.column("Počet", width=120, stretch=NO,anchor=CENTER)
    tree.column("Popis", width=120,stretch=NO,anchor=CENTER)
    tree.column("Cena za kus", width=120,stretch=NO,anchor=CENTER)
    tree.column("Cena", width=120,stretch=NO,anchor=CENTER)

    tree.heading("Počet", text="Počet")
    tree.heading("Popis", text="Popis")
    tree.heading("Cena za kus", text="Cena za kus")
    tree.heading("Cena", text="Cena")

    tree.grid(row=999, column=0, padx=1, pady=1, columnspan=3, rowspan=4)

    save_faktura_button = Button(main_frame, text='Generovat fakturu', command=Faktura,width=30)
    save_faktura_button.grid(row=5, column=1)
    save_faktura_button.place(x=250, y=460)

    new_faktura  = Button(main_frame, text="Nová faktura", command=new,width=30)
    new_faktura.place(x=15, y=460)

    frame = Frame(main_frame, bg='white', padx=30, pady=30, borderwidth=2)
    frame.place(relx=0.5, rely=0.5, anchor='center')
    frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)


# --------------------------------------------------------------------------------------------
def stavObjednavky(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(prvniStranaAdmin.HlavniStrana, highlightbackground='black', highlightthickness=2)
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
    main_frame.place(x=250, y=50)

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
    FrameZbozi = Frame(prvniStranaAdmin.HlavniStrana, bg='white')
    FrameZbozi.place(x=500, y=150, anchor='center')
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

    refreshframe = Frame(prvniStranaAdmin.HlavniStrana, bg='white')
    refreshframe.place(x=680,y=350, anchor='center')
    refreshframe.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)

    refresh_button = tk.Button(refreshframe, text="Refresh", font=("Arial", 12), bg="white", fg="black",
                               command=lambda :stavObjednavky(prvniStranaAdmin.HlavniStrana))
    refresh_button.grid(pady=10, padx=10)

    messageLabel = Label(prvniStranaAdmin.HlavniStrana, text='Mazání záznamů', bg='light grey')
    messageLabel.place(x=450, y=10, height=35)


# --------------------------------------------------------------------------------------------
# Button objednavky
objednavkaButton = Button(prvniStranaAdmin.HlavniStrana, text='Objednávky', font=('Open Sans', 13, 'bold'),
                          fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                          ,  width=19, command=lambda: ikona(objednavka_ikona, objednavka(prvniStranaAdmin.main_frame)))
objednavkaButton.place(x=30, y=70)

objednavka_ikona = Label(prvniStranaAdmin.HlavniStrana, text='', bg='#c3c3c3')
objednavka_ikona.place(x=25, y=69, height=35)

# --------------------------------------------------------------------------------------------
# button pro kontrolu poslanych objednavek
stavObjednavkyButton = Button(prvniStranaAdmin.HlavniStrana, text='Stav objednávky', font=('Open Sans', 13, 'bold'),
                              fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                              , width=19, command=lambda: ikona(stavobjednavky_ikona,stavObjednavky(prvniStranaAdmin.main_frame)))

stavObjednavkyButton.pack()
stavObjednavkyButton.place(x=30, y=370)

stavobjednavky_ikona = Label(prvniStranaAdmin.HlavniStrana, text='', bg='#c3c3c3')
stavobjednavky_ikona.place(x=25, y=369, height=35)

