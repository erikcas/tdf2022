import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class myFormatter(matplotlib.ticker.Formatter):
    def __call__(self,in_value_in_seconds,pos=None):
        hours = int(in_value_in_seconds//(3600))
        in_value_in_seconds -= hours * 3600
        mins = int(in_value_in_seconds//(60))
        in_value_in_seconds -= mins * 60
        secs = int(in_value_in_seconds)

        #return str(hours) + ":" + str(mins) + ":" + str(secs)
        return '%02d:%02d:%02d' % (hours, mins, secs)

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
    graph_date = date.apply(lambda x: datetime.strptime(x, '%d_%m_%Y').strftime('%d-%m-%Y'))
    # return the string of the date, instead of its type and object
    # Stackoverflow again to the rescue!
    # https://stackoverflow.com/questions/39578466/pandas-date-to-string
    date = date.astype(str).tail(1).reset_index().loc[0, 'date']
    graph_date = graph_date.astype(str).tail(1).reset_index().loc[0, 'date']

    return date, graph_date

def etappe_afstand(stage):
    etappe = open_etappe(stage)
    afstand = etappe['lengthDisplay']
    # Return the value as a float. Again very helpfull:
    # # https://stackoverflow.com/questions/39578466/pandas-date-to-string
    afstand = afstand.astype(float).tail(1).reset_index().loc[0, 'lengthDisplay']
    
    return afstand

def prep_data(ruwe_data, rugnr):
    data_renner = ruwe_data[ruwe_data['Bib'] == rugnr]
    data_renner = data_renner[data_renner['Status'].astype(str).str.match(str('active')) == True]

    return data_renner

def prep_afstand(data_renner, afstand):
    for x in data_renner.index:
        nogtegaan = data_renner.loc[x, 'kmToFinish']
        data_renner.loc[x, 'AfgelegdeAfstand'] = afstand - nogtegaan

    return data_renner

def prep_tijd(ruwe_data, rugnr, afstand):
    data_renner = prep_data(ruwe_data, rugnr)
    afstand_renner = prep_afstand(data_renner, afstand)
    starttijd = afstand_renner.iloc[0, afstand_renner.columns.get_loc('TimeStamp')]
    for x in afstand_renner.index:
        tijd_renner = afstand_renner.loc[x, 'TimeStamp']
        temp = int(tijd_renner) - int(starttijd)
        afstand_renner.loc[x, 'Tijd'] = temp
 
    return afstand_renner

def maak_grafiek(renner1, renner2, etappe):
    rugnr1 = zoek_rugnr(renner1)
    rugnr2 = zoek_rugnr(renner2)
    etappenr, datum_etappe = etappe_datum(etappe)
    afstand = etappe_afstand(etappe)
    ruwe_data = pd.read_csv(f'renners_telemetry_{etappenr}.csv', sep=',')
    data_renner1 = prep_tijd(ruwe_data, rugnr1, afstand)
    data_renner2 = prep_tijd(ruwe_data, rugnr2, afstand)

    for frame in [data_renner1, data_renner2]:
        r1 = list(data_renner1['Tijd'])
        r2 = list(data_renner2['Tijd'])
        km1 = list(data_renner1['AfgelegdeAfstand'])
        km2 = list(data_renner2['AfgelegdeAfstand'])

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(r1, km1, c='red',label=renner1)
    ax.plot(r2, km2, c='blue',label=renner2)

    # Format plot
    plt.title(f'TDF2022 | etappe {etappe} | datum {datum_etappe}.\n{renner1} vs {renner2}', fontsize=16)
    plt.xlabel('Tijd', fontsize=12)
    fig.autofmt_xdate()
    plt.ylabel('Kilometers', fontsize=12)
    plt.tick_params(axis='both', which='major', labelsize=16)
    datum_format = myFormatter()
    ax.xaxis.set_major_formatter(datum_format)
    plt.legend(loc='best')
    plt.show()
