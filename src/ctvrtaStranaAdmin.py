

import druhaStranaAdmin
import tretiStranaAdmin


from tkinter import *
import tkinter as tk
import pymysql
import prvniStranaAdmin
import druhaStranaAdmin



def hide_ikona():
    tretiStranaAdmin.objednavka_ikona.config(bg='#c3c3c3')
    tretiStranaAdmin.stavobjednavky_ikona.config(bg='#c3c3c3')
    druhaStranaAdmin.poznamky_ikona.config(bg='#c3c3c3')
    druhaStranaAdmin.prava_ikona.config(bg='#c3c3c3')
    hesla_ikona.config(bg='#c3c3c3')

# --------------------------------------------------------------------------------------------
def ikona(lb, page):
    hide_ikona()
    lb.config(bg='black')
    page()


# --------------------------------------------------------------------------------------------

def kontrolaHeselmetoda(ctverec):
    ctverec.tkraise()
    main_frame = tk.Frame(prvniStranaAdmin.HlavniStrana, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=tk.RIGHT)
    main_frame.pack_propagate(False)
    main_frame.configure(height=500, width=500)
    main_frame.place(x=262, y=180)
    header_bg_color = '#8ac6d1'
    header_fg_color = 'white'
    row_bg_color_1 = '#f0f0f0'
    row_bg_color_2 = 'white'
    conn = pymysql.connect(host='localhost', user='root')
    mycursor = conn.cursor()
    query = 'use uzivatelskaData'
    mycursor.execute(query)
    query = 'select * from uzivatel'
    mycursor.execute(query)
    i = 1
    for uzivatel in mycursor:
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

            e = Label(main_frame, width=15, text='Id', borderwidth=5, relief='ridge', anchor='w', bg=label_bg_color,
                      fg=label_fg_color)
            e.grid(row=0, column=0)
            e = Label(main_frame, width=15, text='Username', borderwidth=5, relief='ridge', anchor='w',
                      bg=label_bg_color, fg=label_fg_color)
            e.grid(row=0, column=1)
            e = Label(main_frame, width=15, text='Password', borderwidth=5, relief='ridge', anchor='w',
                      bg=label_bg_color, fg=label_fg_color)
            e.grid(row=0, column=2)
            e = Label(main_frame, width=15, text='Role', borderwidth=5, relief='ridge', anchor='w',
                      bg=label_bg_color, fg=label_fg_color)
            e.grid(row=0, column=3)
            e = Label(main_frame, width=15, fg='black', borderwidth=3, relief='ridge', anchor="w", text=uzivatel[j],
                      bg=row_bg_color)
            e.grid(row=i, column=j)
        i += 1
    frame1 = Frame(main_frame, bg='white')
    frame1.place(x=200, y=300)

# --------------------------------------------------------------------------------------------
#button pro kontrolu hesel
heslaButton = Button(prvniStranaAdmin.HlavniStrana, text='Kontrola hesel', font=('Open Sans', 13, 'bold'),
                     fg='black', bg='white', activeforeground='grey', activebackground='white', cursor='hand2'
                     , bd=1, width=19, command=lambda: ikona(hesla_ikona, kontrolaHeselmetoda(prvniStranaAdmin.main_frame)))
heslaButton.pack()
heslaButton.place(x=30, y=250)

hesla_ikona = Label(prvniStranaAdmin.HlavniStrana, text ='', bg='#c3c3c3')
hesla_ikona.place(x=25, y=249, height=35)

prvniStranaAdmin.HlavniStrana.mainloop()
