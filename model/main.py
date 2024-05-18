import pandas as pd
import numpy as np
from convertData import convertDataService


def getDataTemperature():
    print()


def convertObjectFieldToNumber(df: pd.DataFrame):
    df.phenomenon = convertDataService.convertPhenomenonColumn(df.phenomenon)
    df.date = convertDataService.convertDateColumn(df.date)
    df.sedges = convertDataService.convertSedgesColumn(df.sedges)
    df.cloudiness = convertDataService.convertCloudinessColumn(df.cloudiness)
    print(df.head(30))

def deleteNight(df: pd.DataFrame):
    return df[df['date'].dt.hour >= 9]

def main():
    pd.set_option('display.max_columns', None)
    df = pd.read_excel('./assets/valid_data.xlsx')
    df = df.rename(
        columns={'WW': 'phenomenon', 'Местное время в Санкт-Петербурге': 'date', 'T': 'temperature', 'U': 'humidity',
                 'Ff': 'windSpeed', 'N': 'cloudiness', 'VV': 'visibility', 'RRR': 'sedges'})
    convertObjectFieldToNumber(df)
    df = deleteNight(df)


main()
