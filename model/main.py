import pandas as pd
import numpy as np
from convertData import convertDataService


def getDataTemperature():
    print()


def convertObjectFieldToNumber(df: pd.DataFrame):
    df.phenomenon = convertDataService.convertPhenomenonColumn(df.phenomenon)
    df.date = convertDataService.convertDateColumn(df.date)
    print(df.head(6))


def main():
    pd.set_option('display.max_columns', None)
    df = pd.read_excel('./assets/valid_data.xlsx')
    df = df.rename(
        columns={'WW': 'phenomenon', 'Местное время в Санкт-Петербурге': 'date', 'T': 'temperature', 'U': 'humidity',
                 'Ff': 'windSpeed', 'N': 'cloudiness', 'VV': 'visibility', 'RRR': 'sedges'})
    print(df.info())
    convertObjectFieldToNumber(df)


main()
