import datetime
import json
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk

import pymysql
from docxtpl import DocxTemplate


def hide_ikona():
    objednavka_ikona.config(bg='#c3c3c3')

# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()

# --------------------------------------------------------------------------------------------

def objednavka(ctverec):
    ctverec.tkraise()
    main_frame = Frame(Objednavka, highlightbackground='black', highlightthickness=2)
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
    ostatniFrame = Frame(Objednavka)
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

    treeFrame = Frame(Objednavka)
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



Objednavka = Tk()
Objednavka.title('Hlavní strana')
Objednavka.resizable(False, False)
options_frame = tk.Frame(Objednavka, bg='#c3c3c3')
options_frame.pack(side=tk.RIGHT)
options_frame.pack_propagate(False)
window_width = 750
window_height = 500
screen_width = Objednavka.winfo_screenwidth()
screen_height = Objednavka.winfo_screenheight()

x_axis = (screen_width / 2) - (window_width / 2)
y_axis = (screen_height / 2) - (window_height / 2)

Objednavka.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_axis), int(y_axis)))

#Zjištění velikosti monitoru pro centrování
#print(screen_width)
#print(screen_height)

main_frame = tk.Frame(Objednavka, highlightbackground='black', highlightthickness=2)
main_frame.pack(side=tk.RIGHT)
main_frame.pack_propagate(False)
main_frame.configure(height=500, width=500)

# --------------------------------------------------------------------------------------------
# Button objednavky
objednavkaButton = Button(Objednavka, text='Objednávky', font=('Open Sans', 13, 'bold'),
                          fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                          ,  width=19, command=lambda: ikona(objednavka_ikona, objednavka(main_frame)))
objednavkaButton.place(x=30, y=70)

objednavka_ikona = Label(Objednavka, text='', bg='#c3c3c3')
objednavka_ikona.place(x=25, y=69, height=35)


