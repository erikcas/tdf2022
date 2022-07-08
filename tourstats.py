from tkinter import *
from tkinter import ttk
from datetime import datetime
from tkinter.messagebox import showinfo
from labelprep import *
from create_stats import maak_grafiek

def prepare_tourstat(renner1, renner2, etappes):
    renner1 = renner1.get()
    renner2 = renner2.get()
    etappe = etappes.get()

    maak_grafiek(renner1, renner2, etappe)

# Maak de GUI

opties = {'padx': 10, 'pady': 10}

class main_app(Tk):
    def __init__(self):
        super().__init__()

        # Creëer het hoofdscherm
        self.title('Tourknutsels1')
        self.geometry('900x550')
        self.resizable(False, False)


class Input_Frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_input()

    def __create_input(self):

        # Renner 1. Wat willen we weten?
        renner_label = ttk.Label(self, text='Renner 1')
        renner_label.grid(column=0, row=1, sticky=(W), **opties)

        # Lijstje der renners
        renner1 = StringVar()
        renner_keuze = ttk.Combobox(self,textvariable=renner1)
        rennerlijst = list_renners()
        renner_keuze['values'] = rennerlijst
        renner_keuze['state'] = 'readonly'
        renner_keuze.grid(column=1, row=1, sticky=(W), **opties)

        # Renner 2. Wat willen we weten?
        renner_label = ttk.Label(self, text='Renner 2')
        renner_label.grid(column=0, row=2, sticky=(W), **opties)

        # Lijstje der renners
        renner2 = StringVar()
        renner_keuze = ttk.Combobox(self,textvariable=renner2)
        rennerlijst = list_renners()
        renner_keuze['values'] = rennerlijst
        renner_keuze['state'] = 'readonly'
        renner_keuze.grid(column=1, row=2, sticky=(W), **opties)

        # Welke etappe. Wat willen we weten?
        etappe_label = ttk.Label(self, text='Welke etappe doen we')
        etappe_label.grid(column=0, row=3, sticky=(W), **opties)

        # Lijstje der etappes
        etappes = StringVar()
        etappe_keuze = ttk.Combobox(self,textvariable=etappes)
        etappelijst = list_etappes()
        etappe_keuze['values'] = etappelijst
        etappe_keuze['state'] = 'readonly'
        etappe_keuze.grid(column=1, row=3, sticky=(W), **opties)

        go_button = ttk.Button(self, text='Vergelijk!',
                command=lambda: prepare_tourstat(renner1, renner2, etappes))
        go_button.grid(column=3, row=3, sticky =EW, **opties)

        self.grid(padx=10, pady=10, sticky=(NSEW))

if __name__ == '__main__':
    app = main_app()
    Input_Frame(app)
    app.mainloop()
