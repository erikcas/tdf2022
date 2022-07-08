import pandas as pd
import numpy as np

def list_etappes():
    filename = 'etappes.csv'
    header = ['stage', 'date']
    # lees etappenummer en datum
    df = pd.read_csv(filename, usecols=header)
    # sorteer van laag naar hoog
    df.sort_values(by=['date'], inplace=True)
    # zet om naar een python dictionary
    lijst = df.set_index('stage')['date'].to_dict()
    etappes = []
    for key, value in lijst.items():
        temp = (key)
        etappes.append(temp)

    return etappes

def list_renners():
    filename = 'rijders.csv'
    # lees de kolommen startnummer (bib) en achternaam
    header = ['bib', 'lastnameshort']
    df = pd.read_csv(filename, usecols=header)
    # verwijder rijen met lege rugnummers
    df['bib'].replace('', np.nan, inplace=True)
    df.dropna(subset=['bib'], inplace=True)
    # zet de rugnummers om van string naar int type
    df['bib'] = df['bib'].astype('int')
    # sorteer op achternaam
    df.sort_values(by=['lastnameshort'], inplace=True)
    # zet om naar een python dictionary
    lijst = df.set_index('bib')['lastnameshort'].to_dict()
    # maak van deze dictionary een lijst
    renners=[]
    for key, value in lijst.items():
        temp = (value)
        renners.append(temp)

    return renners
