import pymysql
from tkinter import Label, Entry, Text, Button, Frame, messagebox

import ObjednavkaStranajedna
import json
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import messagebox



def hide_ikona():
    poznamky_ikona.config(bg='#c3c3c3')
    zaloha_ikona.config(bg='#c3c3c3')


# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()




# --------------------------------------------------------------------------------------------
def poznamky(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightbackground='black', highlightthickness=2)
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
def Zaloha(ctverec):
    def delete(row):
        my_var = messagebox.askyesnocancel("Smazání", "Opravdu chcete tento záznam smazat?", icon="warning",
                                           default="no")
        if my_var:
            conn = pymysql.connect(host='localhost', user='root', password='', database='uzivatelskadata')
            mycursor = conn.cursor()
            # Delete row from database
            r_set = 'DELETE FROM email where poznamka =%s'
            mycursor.execute(r_set, row[5])
            conn.commit()
            # Remove widgets from the main_frame
            for j in range(len(row)):
                e = Label(main_frame, width=8, fg='black', borderwidth=4, relief='ridge', anchor="center", text='x')
            messagebox.showerror("Smazání", "Smazání záznamu proběhlo v pořádku")
    def refresh_table():
        main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightbackground='black', highlightthickness=2)
        main_frame.pack(side=tk.RIGHT)
        main_frame.pack_propagate(False)
        main_frame.place(x=250, y=208)
        for widget in main_frame.winfo_children():
            widget.destroy()
    def otevritEmail():
        otevrit = tk.Tk()
        otevrit.title('Email')
        otevrit.resizable(False, False)
        window_width = 465
        window_height = 300
        screen_width = ObjednavkaStranajedna.Objednavka.winfo_screenwidth()
        screen_height = ObjednavkaStranajedna.Objednavka.winfo_screenheight()
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
        query = 'use uzivatelskadata'
        mycursor.execute(query)
        query = 'select komu, predmet, poznamka, nutnost from email'
        mycursor.execute(query)
        i = 1
        for email in mycursor:
            for j in range(len(email)):
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
                e = Label(otevrit, width=8, text='Komu', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=0)
                e = Label(otevrit, width=8, text='Předmět', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=1)
                e = Label(otevrit, width=8, text='Poznámka', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=2)
                e = Label(otevrit, width=8, text='Nutnost', borderwidth=5, relief='ridge', anchor='w',
                          bg=label_bg_color, fg=label_fg_color)
                e.grid(row=0, column=3)
                e = Label(otevrit, width=8, fg='black', borderwidth=5, relief='ridge', anchor="w", text=email[j],
                          bg=row_bg_color)
                e.grid(row=i, column=j)
            i += 1
    ctverec.tkraise()
    main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=250, y=0)

    def search_zaznam_sklad():
        main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightthickness=2)
        main_frame.pack_propagate(False)
        main_frame.pack(side=tk.RIGHT)
        main_frame.place(x=260, y=300)
        main_frame.configure(width=500, height=495)

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
            query = "SELECT * FROM email WHERE komu=%s"

            vals = (search_text_var.get())
            cursor.execute(query, vals)
            myRows = cursor.fetchall()
            colums = cursor.fetchmany()
            totalRows = cursor.rowcount

            if myRows == None:
                messagebox.showerror('Error', 'Chybný název emailu')
            else:
                main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightbackground='black', highlightthickness=2)
                main_frame.pack_propagate(False)
                main_frame.place(x=255, y=260)
                header_bg_color = '#8ac6d1'
                header_fg_color = 'white'
                row_bg_color_1 = '#f0f0f0'
                row_bg_color_2 = 'white'
                i = 1

                for email in myRows:
                    for j in range(len(email)):
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

                        e = Label(main_frame, width=7, text='Id', borderwidth=5, relief='ridge', anchor='w', bg=label_bg_color,
                                  fg=label_fg_color)
                        e.grid(row=0, column=0)
                        e = Label(main_frame, width=8, text='Od', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=1)
                        e = Label(main_frame, width=8, text='Komu', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=2)
                        e = Label(main_frame, width=8, text='Předmět', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=3)
                        e = Label(main_frame, width=8, text='Obsah', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=4)
                        e = Label(main_frame, width=8, text='Pozn.', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=5)
                        e = Label(main_frame, width=8, text='Nutnost', borderwidth=5, relief='ridge', anchor='w',
                                  bg=label_bg_color, fg=label_fg_color)
                        e.grid(row=0, column=6)
                        e = Label(main_frame, width=8, fg='black', borderwidth=3, relief='ridge', anchor="w", text=email[j],
                                  bg=row_bg_color)
                        e.grid(row=i, column=j)
                        e = Button(main_frame, text="X", command=lambda row=email: delete(row))
                        e.grid(row=i, column=j + 1)
                    i += 1

    main_frame = tk.Frame(ObjednavkaStranajedna.Objednavka, highlightthickness=2)
    main_frame.pack_propagate(False)
    main_frame.pack(side=tk.RIGHT)
    main_frame.place(x=250, y=90)
    main_frame.configure(width=500, height=495)
    messageLabel = Label(ObjednavkaStranajedna.Objednavka, text='Zadejte, komu byl Email zaslán', bg='light grey')
    messageLabel.place(x=405, y=10, height=37)
    search_text_var = tk.StringVar()
    Zbozi = tk.Entry(main_frame,textvariable=search_text_var)
    buttonSearch = tk.Button(main_frame,text="Search", command=search_zaznam_sklad)
    Zbozi.pack(side='left', padx=5, pady=5)
    buttonSearch.pack(side='left', padx=5, pady=5)
    Zbozi.place(x=150, y=15)
    buttonSearch.place(x=280, y=13)
    refreshframe = Frame(ObjednavkaStranajedna.Objednavka, bg='white')
    refreshframe.place(x=680, y=160, anchor='center')
    refreshframe.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)
    refresh_button = tk.Button(refreshframe, text="Refresh", font=("Arial", 12), bg="white", fg="black",
                               command=lambda: Zaloha(main_frame))
    refresh_button.grid(pady=10, padx=10)
    buttonSearch = tk.Button(main_frame, text="Otevřít emaily v novém okně", command=otevritEmail)
    buttonSearch.pack(side='left', padx=5, pady=5)
    buttonSearch.place(x=150, y=70)
# --------------------------------------------------------------------------------------------



def LogOut():
    ObjednavkaStranajedna.Objednavka.destroy()
# --------------------------------------------------------------------------------------------
# Button k poznamkam
poznamkyButton = Button(ObjednavkaStranajedna.Objednavka, text='Poznámky', font=('Open Sans', 13, 'bold'),
                        fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                        , width=19, command=lambda: ikona(poznamky_ikona, poznamky(ObjednavkaStranajedna.main_frame)))

poznamkyButton.pack()
poznamkyButton.place(x=30, y=420)

poznamky_ikona = Label(ObjednavkaStranajedna.Objednavka, text='', bg='#c3c3c3')
poznamky_ikona.place(x=25, y=419, height=35)

# --------------------------------------------------------------------------------------------
#button pro zalohy
zalohaButton = Button(ObjednavkaStranajedna.Objednavka, text='Záloha', font=('Open Sans', 13, 'bold'),
                     fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                     ,bd=1, width=19, command=lambda: ikona(zaloha_ikona, Zaloha(ObjednavkaStranajedna.main_frame)))
zalohaButton.pack()
zalohaButton.place(x=30, y=240)

zaloha_ikona = Label(ObjednavkaStranajedna.Objednavka, text ='', bg='#c3c3c3')
zaloha_ikona.place(x=25, y=239, height=35)
# --------------------------------------------------------------------------------------------

LogOut = Button(ObjednavkaStranajedna.Objednavka, text="Odhlásit se",font=('Open Sans', 8, 'bold'),
                              fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                              , width=10,command=LogOut)
LogOut.pack()
LogOut.place(x=150,y=10)
