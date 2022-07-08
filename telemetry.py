#!<path/to/your/python
import regex
import json
import requests
import time
from datetime import datetime
import pandas as pd
import os
import logging

logging.basicConfig(filename='telemetry_log.log',
        filemode = 'a',
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=logging.DEBUG)

def streamstage():
    s = requests.Session()
    r = s.get('https://racecenter.letour.fr/live-stream', stream=True)
    date = datetime.now().strftime("%d_%m_%Y")
    filename = f'telemetry_{date}.csv'
    if r.encoding is None:
        r.encoding = 'utf-8'

    text = ''
    for line in r.iter_lines(decode_unicode=True):
        if 'data: {' in line:
            data = line.replace('data: {', '{')
            all_data = json.loads(data)
            # Welke kolommen willen we, unify data
            kolommen = ["Pos", "Bib", "Status", "kmToFinish", "secToFirstRider", "kph", "kphAvg", "Latitude", "Longitude", "degC", "TimeStamp"]
            # renners
            try:
                if all_data['bind'] == 'telemetryCompetitor-2022':
                    logging.debug('[TELEMETRY]: Alweer een [RENNERS] telemetry entry!')
                    renners = all_data['data']['Riders']
                    tijdstip = all_data['data']['TimeStamp']
                    df = pd.DataFrame(renners)
                    df['TimeStamp']=tijdstip
                    renners = f'renners_{filename}'
                    if not os.path.isfile(renners):
                        df.to_csv(renners, columns=kolommen, index=False)
                    else:
                        df.to_csv(renners, mode='a', columns=kolommen, index=False, header=False)
            except Exception as e:
                logging.debug(f'[TELEMETRY][FOUT]: Och hemel! Foutje: {e}')

while True:
    streamstage()
