import pandas as pd
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def zoek_rugnr(naam):
    url = "https://racecenter.letour.fr/api/allCompetitors-2022"
    rugnr = pd.read_json(url)
    rugnr = rugnr[rugnr['lastnameshort'].str.contains(naam)==True]
    bib = rugnr['bib']
    bib = int(bib)
    
    return bib

def open_etappe(stage):
    url = "https://racecenter.letour.fr/api/stage-2022"
    etappe = pd.read_json(url)
    # zoek en selecteer de data van de gewenste etappe.
    etappe = etappe[etappe['stage'].astype(str).str.match(stage)==True]
    
    return etappe

def etappe_datum(stage):
    etappe = open_etappe(stage)
    # zoek de datum en vertaal naar een integer
    date = pd.to_datetime(etappe['date'])
    date = pd.to_datetime(date).dt.date
    date = pd.to_datetime(date, format='%Y-%m-%d').astype(str)
    date = date.apply(lambda x: datetime.strptime(x[:10], '%Y-%m-%d').strftime('%d_%m_%Y'))
    # return the string of the date, instead of its type and object
    # Stackoverflow again to the rescue!
    # https://stackoverflow.com/questions/39578466/pandas-date-to-string
    date = date.astype(str).tail(1).reset_index().loc[0, 'date']

    return date

def etappe_afstand(stage):
    etappe = open_etappe(stage)
    afstand = etappe['lengthDisplay']
    # Return the value as a float. Again very helpfull:
    # # https://stackoverflow.com/questions/39578466/pandas-date-to-string
    afstand = afstand.astype(float).tail(1).reset_index().loc[0, 'lengthDisplay']
    
    return afstand

def maak_grafiek(renner1, renner2, etappe):
    rugnr1 = zoek_rugnr(renner1)
    rugnr2 = zoek_rugnr(renner2)
    etappenr = etappe_datum(etappe)
    afstand = etappe_afstand(etappe)
    ruwe_data = pd.read_csv(f'renners_telemetry_{etappenr}.csv', sep=',')
    data_renner1 = ruwe_data[ruwe_data['Bib'].astype(str).str.match(str(rugnr1)) == True]
    data_renner2 = ruwe_data[ruwe_data['Bib'].astype(str).str.match(str(rugnr2)) == True]
    data_renner1 = data_renner1[ruwe_data['Status'].astype(str).str.match(str('active')) == True]
    data_renner2 = data_renner2[ruwe_data['Status'].astype(str).str.match(str('active')) == True]
    for x in data_renner1.index:
        nogtegaan1 = data_renner1.loc[x, 'kmToFinish']
        #nogtegaan1 = nogtegaan1.astype(float).tail(1).reset_index().loc[0, 'kmToFinish']
        data_renner1.loc[x, 'AfgelegdeAfstand'] = afstand - nogtegaan1
    for x in data_renner2.index:
        nogtegaan2 = data_renner2.loc[x, 'kmToFinish']
        #nogtegaan2 = nogtegaan2.astype(float).tail(1).reset_index().loc[0, 'kmToFinish']
        data_renner2.loc[x, 'AfgelegdeAfstand'] = afstand - nogtegaan2
    for x in data_renner1.index:
        tijd_renner1 = data_renner1.loc[x, 'TimeStamp']
        data_renner1.loc[x, 'Tijd'] = time.strftime('%H:%M:%S', time.localtime(tijd_renner1))
    for x in data_renner2.index:
        tijd_renner2 = data_renner2.loc[x, 'TimeStamp']
        data_renner2.loc[x, 'Tijd'] = time.strftime('%H:%M:%S', time.localtime(tijd_renner2))
    data_renner1.to_csv('d1.csv')
    for frame in [data_renner1, data_renner2]:
        plt.plot(frame['Tijd'], frame['AfgelegdeAfstand'])
    #plt.legend(loc=2)
    plt.title('test', fontsize=14)
    #ax.xaxis.set_major_locator(months)
    #ax.xaxis.set_major_formatter(timeFmt)
    #ax.xaxis.set_minor_locator(days)
    plt.show()
