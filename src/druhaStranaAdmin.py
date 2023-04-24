import os.path
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import pymysql
import prvniStranaAdmin
from tkinter import ttk, messagebox
import json




def hide_ikona():
    poznamky_ikona.config(bg='#c3c3c3')
    prava_ikona.config(bg='#c3c3c3')

# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()

# --------------------------------------------------------------------------------------------
def prava(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(prvniStranaAdmin.HlavniStrana, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=250, y=0)

    def delete(row):
        my_var = messagebox.askyesnocancel("Smazání", "Opravdu chcete tento záznam smazat?", icon="warning",
                                           default="no")
        if my_var:
            conn = pymysql.connect(host='localhost', user='root', password='', database='uzivatelskadata')
            mycursor = conn.cursor()
            # Delete row from database
            r_set = 'DELETE FROM uzivatel where username =%s'
            mycursor.execute(r_set,row[1])
            conn.commit()

            # Remove widgets from the main_frame
            for j in range(len(row)):
                e = Label(main_frame, width=8, fg='black', borderwidth=4, relief='ridge', anchor="center", text='x')
            messagebox.showerror("Smazání", "Smazání záznamu proběhlo v pořádku")

    def refresh_table():
        main_frame = tk.Frame(prvniStranaAdmin.HlavniStrana, highlightbackground='black', highlightthickness=2)
        main_frame.pack(side=tk.RIGHT)
        main_frame.pack_propagate(False)
        main_frame.place(x=250, y=208)
        for widget in main_frame.winfo_children():
            widget.destroy()
    def search_zaznam():

        def editing():
            conn = pymysql.connect(host='localhost', user='root')
            cursor = conn.cursor()
            query = 'use uzivatelskadata'
            cursor.execute(query)

            role = {'Admin', 'KS', 'OZ'}

            e1_str_id = StringVar(main_frame)
            e2_str_username = StringVar(main_frame)
            e3_str_password = StringVar(main_frame)
            e4_str_role = StringVar(prvniStranaAdmin.HlavniStrana)
            e4_str_role.set("Role")

            e1_str_id.set(['ID'])
            e2_str_username.set(['Username'])
            e3_str_password.set(['Password'])
            e4_str_role.set(["role"])

            e1 = Entry(main_frame, textvariable=e1_str_id, width=14,
                       fg='black', borderwidth=3, relief='ridge')
            e1.grid(row=2, column=0)
            e2 = Entry(main_frame, textvariable=e2_str_username, width=14,
                       fg='black', borderwidth=3, relief='ridge')
            e2.grid(row=2, column=1)

            e3 = Entry(main_frame, textvariable=e3_str_password, width=14,
                       fg='black', borderwidth=3, relief='ridge')
            e3.grid(row=2, column=2)

            menu = OptionMenu(prvniStranaAdmin.HlavniStrana, e4_str_role, *role)
            menu.place(x=580, y=178)

            def myUpdate():
                def clear2():
                    menu.destroy()
                    main_frame.destroy()
                def clear3():
                    for widget in main_frame.winfo_children():
                            widget.destroy()
                conn = pymysql.connect(host='localhost', user='root')
                cursor = conn.cursor()
                query = 'use uzivatelskadata'
                cursor.execute(query)

                # Vyhledání ID uživatele podle zadaného jména
                search_i = e1_str_id.get()
                select_query = f"SELECT username FROM uzivatel WHERE id='{search_i}'"
                cursor.execute(select_query)
                result = cursor.fetchone()
                if result is None:
                    messagebox.showerror('Error', f"Uživatel s id '{search_i}' nebyl nalezen.")
                    return
                user_id = result[0]

                # Aktualizace záznamu uživatele podle ID
                username = e2_str_username.get()
                password = e3_str_password.get()
                role = e4_str_role.get()
                update_query = f"UPDATE uzivatel SET username='{username}', password='{password}', role='{role}' WHERE id='{search_i}'"
                cursor.execute(update_query)
                conn.commit()

                messagebox.showinfo('Info', "Záznam byl změněn")
                clear2()
                clear()
                clear3()
            bt2 = Button(main_frame, text="Update", command=myUpdate,
                         relief='ridge', anchor='w', width=6, borderwidth=4,
                         bg='light grey', fg=label_fg_color)
            bt2.grid(row=2, column=5)
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
            query = "SELECT * FROM uzivatel WHERE username=%s"

            vals = (search_text_var.get())
            cursor.execute(query, vals)
            myRows = cursor.fetchall()
            totalRows = cursor.rowcount

            def clear():
                searchUzivatel.delete(0, END)

            if myRows == None:
                messagebox.showerror('Error', 'Chybné uživatelské jméno nebo heslo')
                clear()
            else:
                main_frame = tk.Frame(prvniStranaAdmin.HlavniStrana, highlightbackground='black', highlightthickness=2)
                main_frame.pack_propagate(False)
                main_frame.place(x=280, y=120)
                header_bg_color = '#8ac6d1'
                header_fg_color = 'white'
                row_bg_color_1 = '#f0f0f0'
                row_bg_color_2 = 'white'
                i = 1



                for uzivatel in myRows:
                    for j in range(len(uzivatel)):
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

                        e = Label(main_frame, width=12, text='Id', borderwidth=5, relief='ridge', anchor='w',
                                  bg='light grey',
                                  fg=label_fg_color)
                        e.grid(row=0, column=0)
                        e = Label(main_frame, width=12, text='Username', borderwidth=5, relief='ridge', anchor='w',
                                  bg='light grey',
                                  fg=label_fg_color)
                        e.grid(row=0, column=1)
                        e = Label(main_frame, width=12, text='Password', borderwidth=5, relief='ridge', anchor='w',
                                  bg='light grey',
                                  fg=label_fg_color)
                        e.grid(row=0, column=2)
                        e = Label(main_frame, width=12, text='Role', borderwidth=5, relief='ridge', anchor='w',
                                  bg='light grey',
                                  fg=label_fg_color)
                        e.grid(row=0, column=3)
                        e = Label(main_frame, width=12, fg='black', borderwidth=3, relief='ridge', anchor="w",
                                  text=uzivatel[j],
                                  bg=row_bg_color)
                        e.grid(row=i, column=j)
                        e = Button(main_frame, width=6, text='Edit', borderwidth=4, relief='ridge', anchor='w',
                                   command=editing,
                                   bg='light grey', fg=label_fg_color)
                        e.grid(row=1, column=5)
                        e = Button(main_frame, text="X", command=lambda row=uzivatel: delete(row))
                        e.grid(row=i, column=j + 1)
                    i += 1


    messageLabel = Label(main_frame, text='Zadejte Username požadované osoby', bg='light grey')
    messageLabel.place(x=138, y=10, height=35)


    search_text_var = tk.StringVar()
    searchUzivatel = tk.Entry(main_frame,textvariable=search_text_var)
    buttonSearch = tk.Button(main_frame,text="Search", command=search_zaznam)
    searchUzivatel.pack(side='left', padx=5, pady=5)
    buttonSearch.pack(side='left', padx=5, pady=5)
    searchUzivatel.place(x=150, y=70)
    buttonSearch.place(x=280, y=65)

    refreshframe = Frame(prvniStranaAdmin.HlavniStrana, bg='white')
    refreshframe.place(x=680, y=260, anchor='center')
    refreshframe.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)
    refresh_button = tk.Button(refreshframe, text="Refresh", font=("Arial", 12), bg="white", fg="black",
                               command=lambda: prava(main_frame))
    refresh_button.grid(pady=10, padx=10)


    def user_enter(event):
        if search_text_var.get() == 'Přihlašovací jméno':
            search_text_var.delete(0, END)

    message = '''
    Návod pro nováčky: 
    - po zadání edit, do kolonky ID zadejte
    id uživatele, kterého chcete změnit. Dále měňte
    dle své libosti.

    Informace k právům:
    Admin - All
    Kontrolor skladu (KS) - zboží a doplnění zboží 
                            do systému
    Objednávky (OZ) - kontrola objednávek a jejich
                       založení
     '''

    text_box = Text(
        main_frame,
        height=14,
        width=61
    )
    text_box.place(x=0, y=300)
    text_box.insert('end', message)
    text_box.config(state='disabled')



# --------------------------------------------------------------------------------------------
def poznamky(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(prvniStranaAdmin.HlavniStrana, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=250, y=0)

    style = ttk.Style()

    style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))
    notebook = ttk.Notebook(main_frame, style="TNotebook")
    notes = {}
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        pass

    notebook = ttk.Notebook(main_frame)
    notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def add_note():
        note_frame = ttk.Frame(notebook, padding=10)
        notebook.add(note_frame, text="New note")

        title_label = ttk.Label(note_frame, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        title_entry = ttk.Entry(note_frame, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=10)

        content_label = ttk.Label(note_frame, text="Text:")
        content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        content_entry = tk.Text(note_frame, width=40, height=10)
        content_entry.grid(row=1, column=1, padx=10, pady=10)

        def save_note():
            title = title_entry.get()
            content = content_entry.get("1.0", tk.END)

            notes[title] = content.strip()
            with open("notes.json", "w") as f:
                json.dump(notes, f)

            note_content = tk.Text(notebook, width=40, height=10)
            note_content.insert(tk.END, content)
            notebook.forget(notebook.select())
            notebook.add(note_content, text=title)

        saveButton = ttk.Button(note_frame, text="Save",
                                command=save_note)
        saveButton.grid(row=2, column=1, padx=10, pady=10)

    def load():
        try:
            with open("notes.json", "r") as f:
                notes = json.load(f)

            for title, content in notes.items():
                note_content = tk.Text(notebook, width=40, height=10)
                note_content.insert(tk.END, content)
                notebook.add(note_content, text=title)

        except FileNotFoundError:
            pass

    load()

    def delete():
        current_tab = notebook.index(notebook.select())
        note_title = notebook.tab(current_tab, "text")
        confirm = messagebox.askyesno("Smazání poznámky",
                                      f"Opravdu chcete poznámku {note_title} smazat?")

        if confirm:
            notebook.forget(current_tab)
            notes.pop(note_title)
            with open("notes.json", "w") as f:
                json.dump(notes, f)

    new_Button = ttk.Button(main_frame, text="New note",
                            command=add_note)
    new_Button.pack(side=tk.LEFT, padx=10, pady=10)
    delete_Button = ttk.Button(main_frame, text="Delete",
                               command=delete, style="primary.TButton")
    delete_Button.pack(side=tk.LEFT, padx=10, pady=10)



# --------------------------------------------------------------------------------------------
# Button k pridani prav
pravaButton = Button(prvniStranaAdmin.HlavniStrana, text='Práva a nastavení', font=('Open Sans', 13, 'bold'),
                     fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                     , width=19, command= lambda: ikona(prava_ikona,prava(prvniStranaAdmin.main_frame)))
pravaButton.pack()
pravaButton.place(x=30, y=130)

prava_ikona = Label(prvniStranaAdmin.HlavniStrana, text='', bg='#c3c3c3')
prava_ikona.place(x=25, y=129, height=35)



# --------------------------------------------------------------------------------------------
# Button k poznamkam
poznamkyButton = Button(prvniStranaAdmin.HlavniStrana, text='Poznámky', font=('Open Sans', 13, 'bold'),
                        fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                        , width=19, command=lambda: ikona(poznamky_ikona, poznamky(prvniStranaAdmin.main_frame)))

poznamkyButton.pack()
poznamkyButton.place(x=30, y=430)

poznamky_ikona = Label(prvniStranaAdmin.HlavniStrana, text='', bg='#c3c3c3')
poznamky_ikona.place(x=25, y=429, height=35)
