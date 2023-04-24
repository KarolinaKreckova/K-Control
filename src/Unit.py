import json
import unittest
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import END
from unittest.mock import patch, mock_open, MagicMock

import pymysql

import ObjednavkaStranaDva
import ObjednavkastranaTri
import druhaStranaAdmin
import prvniStranaAdmin

class PridatZamTest(unittest.TestCase):
    def setUp(self):
        self.app = tk.Tk()

    def tearDown(self):
        self.app.destroy()

    def test_pridatZam(self):
        self.assertEqual(prvniStranaAdmin.pridatZam(tk.Frame()), None)

    def test_pridatZam_empty(self):
        with self.assertRaises(messagebox.showerror):
            prvniStranaAdmin.pridatZam(tk.Frame(username="", password="", password_confirm="", check=0))

    def test_pridatZam_wrong_password(self):
        with self.assertRaises(messagebox.showerror):
            prvniStranaAdmin.pridatZam(tk.Frame(username="Test", password="test", password_confirm="wrongtest", check=1))

    def test_pridatZam_insert(self):
        conn = pymysql.connect(host='localhost', user='root')
        mycursor = conn.cursor()
        mycursor.execute("DROP DATABASE IF EXISTS uzivatelskadata")
        mycursor.execute("CREATE DATABASE uzivatelskadata")
        mycursor.execute("USE uzivatelskadata")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS uzivatel (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, username VARCHAR (50), password VARCHAR(40), role VARCHAR(45))")
        mycursor.execute("INSERT INTO uzivatel(username, password) VALUES ('Test', 'test')")
        conn.commit()
        conn.close()

        prvniStranaAdmin.pridatZam(tk.Frame(username="Test", password="test", password_confirm="test", check=1))

        conn = pymysql.connect(host='localhost', user='root')
        mycursor = conn.cursor()
        mycursor.execute("USE uzivatelskadata")
        mycursor.execute("SELECT * FROM uzivatel WHERE username='Test'")
        result = mycursor.fetchone()
        conn.commit()
        conn.close()

        self.assertIsNotNone(result)


class ZalohaTest(unittest.TestCase):
    def setUp(self):
        self.app = tk.Tk()
        self.app.withdraw()

    def tearDown(self):
        self.app.update()
        self.app.quit()

    def test_search_zaznam_sklad_error(self):
        search_text_var = tk.StringVar()
        search_text_var.set('')
        messagebox.showerror =tk.MagicMock()

        with self.assertRaises(TypeError):
            prvniStranaAdmin.Zaloha(search_text_var)

        messagebox.showerror.assert_called_with('Error', 'Vyplňte všechna pole')

    def test_search_zaznam_sklad(self):
        search_text_var = tk.StringVar()
        search_text_var.set('test@email.com')
        Objednavka = tk.Tk()
        main_frame = tk.Frame(Objednavka)
        main_frame.pack()
        messagebox.showerror = tk.MagicMock()
        conn = pymysql.connect(host='localhost', user='root')
        cursor = conn.cursor()
        cursor.execute('use uzivatelskadata')
        cursor.execute("SELECT * FROM email WHERE komu=%s", (search_text_var.get(),))
        myRows = cursor.fetchall()
        totalRows = cursor.rowcount

        prvniStranaAdmin.Zaloha(search_text_var)

        self.assertEqual(len(myRows), totalRows)
        self.assertTrue(main_frame.winfo_ismapped())

class TestPrava(unittest.TestCase):
    def test_prava(self):
        root = tk.Tk()
        prvniStranaAdmin = tk.Frame(root)
        prvniStranaAdmin.HlavniStrana = tk.Frame(root)
        ctverec = tk.Frame(prvniStranaAdmin.HlavniStrana)

        druhaStranaAdmin.prava(ctverec)

        main_frame = prvniStranaAdmin.HlavniStrana.winfo_children()[0]
        self.assertIsInstance(main_frame, tk.Frame)
        self.assertEqual(main_frame['highlightbackground'], 'black')
        self.assertEqual(main_frame['highlightthickness'], 2)
        self.assertEqual(main_frame.winfo_width(), 500)
        self.assertEqual(main_frame.winfo_height(), 500)

        row = ['1', 'test_user', 'test_password']
        druhaStranaAdmin.delete(row)
        conn = pymysql.connect(host='localhost', user='root', password='', database='uzivatelskadata')
        mycursor = conn.cursor()
        mycursor.execute('SELECT * FROM uzivatel WHERE username=%s', ('test_user',))
        result = mycursor.fetchone()
        self.assertIsNone(result)

        druhaStranaAdmin.refresh_table()
        self.assertEqual(len(main_frame.winfo_children()), 0)

        search_text_var = tk.StringVar()
        search_text_var.set('test_user')
        druhaStranaAdmin.search_zaznam()
        self.assertIsInstance(main_frame, tk.Frame)
        self.assertEqual(main_frame['highlightbackground'], 'black')
        self.assertEqual(main_frame['highlightthickness'], 2)
        self.assertEqual(main_frame.winfo_width(), 500)
        self.assertEqual(main_frame.winfo_height(), 500)

        druhaStranaAdmin.editing()
        self.assertIsInstance(main_frame, tk.Frame)
        self.assertEqual(main_frame['highlightbackground'], 'black')
        self.assertEqual(main_frame['highlightthickness'], 2)
        self.assertEqual(main_frame.winfo_width(), 500)
        self.assertEqual(main_frame.winfo_height(), 500)


class TestPoznamky(unittest.TestCase):

    def setUp(self):
        self.ctverec = tk.Tk()
        prvniStranaAdmin = tk.Frame(self.ctverec)
        HlavniStrana = tk.Frame(prvniStranaAdmin)
        self.ctverec.frames = {HlavniStrana}

    @patch('builtins.open', new_callable=mock_open)
    def test_load(self, mock_file):
        mock_file.return_value.read.return_value = '{"Poznamka1": "Poznamka 1", "Poznamka2": "Poznamka 2"}'
        notes = {}
        druhaStranaAdmin.poznamky.load(notes)
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes['Poznamka1'], 'Poznamka 1')
        self.assertEqual(notes['Poznamka2'], 'Poznamka 2')

    @patch('builtins.open', new_callable=mock_open)
    def test_save(self, mock_file):
        notes = {'Poznamka1': 'Poznamka 1', 'Poznamka2': 'Poznamka 2'}
        druhaStranaAdmin.poznamky.save(notes)
        mock_file.assert_called_once_with('notes.json', 'w')
        handle = mock_file()
        handle.write.assert_called_once_with(json.dumps(notes))

    @patch.object(messagebox, 'askyesno')
    def test_delete(self, mock_askyesno):
        notes = {'Poznamka1': 'Poznamka 1', 'Poznamka2': 'Poznamka2'}
        mock_askyesno.return_value = True
        druhaStranaAdmin.poznamky.delete(notes, 'Poznamka1')
        self.assertEqual(len(notes), 1)
        self.assertNotIn('note1', notes)
        mock_askyesno.assert_called_once_with(
            "Smazání poznámky",
            "Opravdu chcete poznámku Poznamka1 smazat?"
        )

    def test_add_note(self):
        notebook = ttk.Notebook(tk.Frame())
        notebook.add = tk.Frame()
        notebook.select = lambda: 0
        notes = {}
        druhaStranaAdmin.poznamky.add_note(notebook, notes)
        self.assertEqual(len(notes), 1)
        self.assertIn('New note', notes.keys())
        self.assertIn('New note', [t['text'] for t in notebook.tabs()])


class TestEmail(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.Objednavka = tk.Frame(self.root)
        ObjednavkaStranaDva = tk.Frame(self.Objednavka)
        self.messagebox_calls = []

        def mock_showerror(title, message):
            self.messagebox_calls.append((title, message))

        def mock_showinfo(title, message):
            self.messagebox_calls.append((title, message))

        messagebox.showerror = mock_showerror
        messagebox.showinfo = mock_showinfo

    def tearDown(self):
        self.root.destroy()

    def test_valid_input(self):
        ctverec = tk.Frame(self.Objednavka)
        OdesilatelAddEntry = tk.Entry(self.Objednavka)
        KomuAddEntry = tk.Entry(self.Objednavka)
        PredmetAddEntry = tk.Entry(self.Objednavka)
        ObsahAddEntry = tk.Entry(self.Objednavka)
        PoznamkaAddEntry = tk.Entry(self.Objednavka)
        NutnostAddEntry = tk.Entry(self.Objednavka)
        check = tk.IntVar()
        ObjednavkaStranaDva.Email(ctverec)
        OdesilatelAddEntry.insert(0, "test@example.com")
        KomuAddEntry.insert(0, "test@example.com")
        PredmetAddEntry.insert(0, "Test email")
        ObsahAddEntry.insert(0, "Test message")
        PoznamkaAddEntry.insert(0, "Test note")
        NutnostAddEntry.insert(0, "1")
        connect_button = self.root.focus_get()
        connect_button.invoke()
        self.assertEqual(len(self.messagebox_calls), 1)
        self.assertEqual(self.messagebox_calls[0][0], "Success")
        self.assertEqual(self.messagebox_calls[0][1], "Záloha emailu proběhla v pořádku")

    def test_empty_input(self):
        ctverec = tk.Frame(self.Objednavka)
        OdesilatelAddEntry = tk.Entry(self.Objednavka)
        KomuAddEntry = tk.Entry(self.Objednavka)
        PredmetAddEntry = tk.Entry(self.Objednavka)
        ObsahAddEntry = tk.Entry(self.Objednavka)
        PoznamkaAddEntry = tk.Entry(self.Objednavka)
        NutnostAddEntry = tk.Entry(self.Objednavka)
        check = tk.IntVar()
        ObjednavkaStranaDva.Email(ctverec)
        connect_button = self.root.focus_get()
        connect_button.invoke()
        self.assertEqual(len(self.messagebox_calls), 1)
        self.assertEqual(self.messagebox_calls[0][0], "Error")
        self.assertEqual(self.messagebox_calls[0][1], "Vyplňte všechna pole")

class TestMethods(unittest.TestCase):

    def test_kontrolaSkladu(self):

        ctverec = MagicMock()
        ctverec.tkraise = MagicMock()

        kontrolorStranajedna = MagicMock()
        kontrolorStranajedna.Kontrola = tk.Frame()
        kontrolorStranajedna.main_frame = tk.Frame()

        kontrolorStranajedna.kontrolaSkladu(ctverec)

        self.assertIsInstance(kontrolorStranajedna.main_frame, tk.Frame)
        self.assertIsInstance(kontrolorStranajedna.main_frame.winfo_children()[0], tk.Label)
        self.assertIsInstance(kontrolorStranajedna.main_frame.winfo_children()[1], tk.Entry)
        self.assertIsInstance(kontrolorStranajedna.main_frame.winfo_children()[2], tk.Entry)
        self.assertIsInstance(kontrolorStranajedna.main_frame.winfo_children()[3], tk.Entry)
        self.assertIsInstance(kontrolorStranajedna.main_frame.winfo_children()[4], tk.Spinbox)
        self.assertIsInstance(kontrolorStranajedna.main_frame.winfo_children()[5], tk.Spinbox)
        self.assertIsInstance(kontrolorStranajedna.main_frame.winfo_children()[6], tk.Button)

        # Check if the function calls are correct
        kontrolorStranajedna.clear_item = MagicMock()
        kontrolorStranajedna.add_item = MagicMock()
        kontrolorStranajedna.delete = MagicMock()
        kontrolorStranajedna.refresh_table = MagicMock()

        kontrolorStranajedna.clear_item.assert_called_once()
        kontrolorStranajedna.add_item.assert_not_called()
        kontrolorStranajedna.delete.assert_not_called()
        kontrolorStranajedna.refresh_table.assert_called_once()


if __name__ == '__main__':
    unittest.main()