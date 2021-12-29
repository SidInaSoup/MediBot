from kivy.factory import Factory
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, ShaderTransition
import sqlite3 as ms
from kivymd.toast import toast
import tkinter as tk
from tkinter import *

fs = """$HEADER
    uniform float t;
    uniform sampler2D tex_in;
    uniform sampler2D tex_out;

    void main(void) {
        vec4 cin = texture2D(tex_in, tex_coord0);
        vec4 cout = texture2D(tex_out, tex_coord0);
        gl_FragColor = mix(cout, cin, t);
    }
"""

tr = ShaderTransition(fs=fs)
sm = ScreenManager(transition=tr)
con = ms.connect('Medibot.db')
cure = None
password = '1'


class DatabaseManager:

    def __init__(self, symptom):
        """
        instantiating symptom array as instances
        :param symptom:
        """
        self.symptom1 = symptom[0]
        self.symptom2 = symptom[1]
        self.symptom3 = symptom[2]
        print(self.symptom1,self.symptom2,self.symptom3)

    def finder(self):
        cur = con.cursor()
        print(self.data)

        try:
            x = f"select * from docdetails where Specialty='{self.data[0][5]}'"
            cur.execute(x)
        except IndexError:

            print()


        data1 = cur.fetchall()
        return data1

    def context_action(self):
        global x1, x2, x3
        flag_1 = True
        cur = con.cursor()

        x1 = f"select * from diseases where (Symptoms1='{self.symptom1}' and Symptoms2='{self.symptom2}');"
        x2 = f"select * from diseases where (Symptoms2='{self.symptom2}' and Symptoms3='{self.symptom3}');"
        x3 = f"select * from diseases where (Symptoms1='{self.symptom1}' and Symptoms3='{self.symptom3}');"

        try:
            cur.execute(x1)

        except:
            toast("Something is wrong with your entries")

        self.data = cur.fetchall()
        print(self.data, '1')
        if self.data!=[]:
            return self.data

        else:
            cur = con.cursor()

            try:
                cur.execute(x2)
            except:
                toast("Something is wrong with your entries")

            self.data = cur.fetchall()
            print(self.data, '2')

            if self.data != []:
                return self.data
            else:
                cur = con.cursor()
                try:
                    cur.execute(x3)
                except:
                    toast("Something is wrong with your entries")

                self.data = cur.fetchall()
                print(self.data, '3')

                if self.data != []:
                    return self.data
                else:
                    cur = con.cursor()
                    if self.symptom1!='':
                        cur.execute(f"select * from diseases where Symptoms1='{self.symptom1}';")
                        self.data = cur.fetchall()
                        print(self.data, 'a')
                    elif self.symptom2!='':
                        cur.execute(f"select * from diseases where Symptoms2='{self.symptom2}';")
                        self.data = cur.fetchall()
                        print(self.data,'b')
                    elif self.symptom3!='':
                        cur.execute(f"select * from diseases where Symptoms3='{self.symptom3}';")
                        self.data = cur.fetchall()
                        print(self.data, 'c')
                    elif self.symptom1!='' or self.symptom2!='' or self.symptom3!='':
                        toast("Please enter a valid entry")
                        flag_1=False
                    else:
                        toast("Please enter atleast one entry")
                        flag_1 = False
                    if flag_1:
                        print(self.data,4)
                        return self.data
                    else:
                        return []



class DatabaseEditor:

    def __init__(self, query, deletionquery):
        self.deletionquery = f'delete from docdetails where Name = "{deletionquery}"'
        self.query = f'insert into docdetails values{query}'

    def table_editor(self):
        cur = con.cursor()
        try:
            cur.execute(self.query)
            con.commit()
            toast("Successfully executed!")
            return 1

        except:
            toast('invalid query')

    def row_deleter(self):
        cur = con.cursor()
        try:
            cur.execute(self.deletionquery)
            con.commit()
            toast('Deleted')
            return 1
        except:
            print('failed query execution(delete)')


class Screen7(Screen):
    def password_change(self):
        global password
        password = self.ids["new_passwd"].text
        self.ids["new_passwd"].text = ''
        toast("Passcode Changed", 3)

    def fade_transition(self):
        global tr, sm
        tr = ShaderTransition(fs=fs)
        sm = ScreenManager(transition=tr)


class Screen6(Screen):
    def confirm_edit(self):
        global dummy, dummy2
        try:
            dummy = DatabaseEditor(self.ids["query_editor"].text, None)
            dummy2 = DatabaseEditor.table_editor(dummy)
            self.ids["query_editor"].text = ''


        except:
            toast('invalid query')

    def delete(self):
        global S
        text = self.ids["query_editor1"].text
        cur = con.cursor()
        cur.execute('select Name from docdetails;')
        docnames = cur.fetchall()
        l = len(docnames)
        try:
            for j in range(l):

                if j == int(text) - 1:
                    S = docnames[j][0]
                else:
                    continue
        except ValueError:
            toast('Please Enter a valid row number')

        delete = DatabaseEditor(None, S)
        delete1 = DatabaseEditor.row_deleter(delete)
        self.ids["query_editor1"].text = ''

    def view_table(self):
        a = TableLoader()
        TableLoader.grid(a)


class Screen5(Screen):
    pass


class Screen4(Screen):
    def authentication(self):
        passcode = password
        if self.ids["adminid"].text == passcode:
            toast('correct passcode')
            self.ids["adminid"].text = ''
            self.manager.current = 'S5'

        else:
            self.ids["adminid"].text = ''
            toast('incorrect passcode')


class Screen3(Screen):
    pass


class Screen1(Screen):
    pass


class Screen2(Screen):

    def info(self):
        print(cure1,cure2)
        try:
            self.ids["number"].text = f"You may be suffering from {cure1[0][0]}.\n The usual treatment for this disease" \
                                      f" is:\n {cure1[0][4]}.\n We suggest you visit:\n {cure2[0][0]}," \
                                      f"\nEducation:{cure2[0][2]},\nPhone:{cure2[0][1]}   "
        except IndexError:
            toast("Sorry Doctor Info not found for this particular symptom")
            self.ids["symp1"].text, self.ids["symp2"].text, self.ids["symp3"].text = '', '', ''



    def reset(self):
        self.ids[
            "number"].text = "\n\nEnter your symptoms in the left.\n MATCH ANY TWO\n Choose from these:\nSymptom1 :1)indigestion;2) " \
                             "Rash;3) Itchy eye; 4)Fever ;5)cough that \n lasts longer than 3 weeks; 6)sore " \
                             "throat,7)sudden fever; 8)diarrhoea;\n 9)sore, red eyes \nSymptom2: 1)nausea and " \
                             "diarrhea; 2)Spots;3) Tearing,Mucus from\n eye;4) Chest pain and shortness of " \
                             "breath; 5)Fever; 6)cough lasts for\n long time; 7)abdominal pain, aching muscles; " \
                             "8)Stomach cramps;\n 9)fever \nSymptom3: 1)abdominal swelling ;  2)Blisters; " \
                             "3)Redness in eye ;\n4)Nausea and vomiting;5) Night sweats;6) aches and pains ;\n " \
                             "7) headache ,  sorethroat;8) vomiting;9) greyish-white spots\n on the inside of " \
                             "cheeks "

        self.ids["symp1"].text, self.ids["symp2"].text, self.ids["symp3"].text = '', '', ''

    def press(self):
        global cure
        global cure1
        global curea
        global cure2

        self.inputbox1 = [self.ids["symp1"].text, self.ids["symp2"].text, self.ids["symp3"].text]
        print(self.inputbox1)
        cure = DatabaseManager(self.inputbox1)
        #try:
        cure1 = DatabaseManager.context_action(cure)
        cure2 = DatabaseManager.finder(cure)
        self.info()
        #except:
            #toast('Invalid input', 2)
            #print()
            #self.ids["symp1"].text, self.ids["symp2"].text, self.ids["symp3"].text = '', '', ''


class Main(MDApp):

    def build(self):
        """

        :rtype: widget
        """
        self.title = "MediBot"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.screen = Builder.load_file('Menudesign.kv')
        self.sm = ScreenManager()

        self.sm.add_widget(Factory.Screen1(name="S1"))
        self.sm.add_widget(Factory.Screen2(name="S2"))
        self.sm.add_widget(Factory.Screen3(name="S3"))
        self.sm.add_widget(Factory.Screen4(name="S4"))
        self.sm.add_widget(Factory.Screen5(name="S5"))
        self.sm.add_widget(Factory.Screen6(name="S6"))
        self.sm.add_widget(Factory.Screen7(name="S7"))
        return self.sm


class TableLoader():
    """To load the table using tkinter"""

    def grid(self):
        my_w = tk.Tk()
        my_w.title("Docdetails database")
        my_w.geometry("600x400")
        cur = con.cursor()
        cur.execute("SELECT * FROM 'docdetails' LIMIT 0,30")
        i = 0
        for student in cur:
            for j in range(len(student)):
                e = Entry(my_w, width=25, fg='blue')
                e.grid(row=i, column=j)
                e.insert(END, student[j])
            i = i + 1

        my_w.mainloop()


if __name__ == '__main__':
    Main().run()
