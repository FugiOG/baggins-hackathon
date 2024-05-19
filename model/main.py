import pandas as pd
from convertData import convertDataService
from seasons import Seasons
import matplotlib.pyplot as plt
# from adtk.detector import ThresholdAD
# from adtk.visualization import plot
from coffeeshop import Coffeeshop
from comfortCalculator import calculateComfortIndex, displayCC

COFFEESHOP_DATA_PATH = './assets/data.xlsx'


def convertObjectFieldToNumber(df: pd.DataFrame):
    df.phenomenon = convertDataService.convertPhenomenonColumn(df.phenomenon)
    df.date = convertDataService.convertDateColumn(df.date)
    df.sedges = convertDataService.convertSedgesColumn(df.sedges)
    df.cloudiness = convertDataService.convertCloudinessColumn(df.cloudiness)


def deleteNight(df: pd.DataFrame):
    return df[df['date'].dt.hour >= 9].reset_index()


def groupRowsByDay(df: pd.DataFrame):
    df['date'] = df['date'].dt.date

    return df.groupby('date').agg(
        {'temperature': 'mean', 'humidity': 'mean', 'windSpeed': 'mean', 'cloudiness': 'mean', 'phenomenon': 'mean',
         'visibility': 'mean', 'sedges': 'mean'}).reset_index()


def enrichWeatherTable(df: pd.DataFrame, coffeeshop):
    return df.merge(coffeeshop, on='date', how='left')

def addComfortCoefficientColumnAlt(df: pd.DataFrame):
    comfortIndeces = []
    for index, row in df.iterrows():
        comfortIndex = calculateComfortIndex(row)
        comfortIndeces.append(comfortIndex)

    coefs = []
    for comfortIndex in comfortIndeces:
        min_ci = min(comfortIndeces)
        max_ci = max(comfortIndeces)
        coef = (comfortIndex - min_ci) / (max_ci - min_ci)
        coefs.append(coef)
    df['CC'] = coefs

    return df

def addComfortCoefficientColumn(df: pd.DataFrame):
    comfortIndeces = []
    for index, row in df.iterrows():
        comfortIndex = calculateComfortIndex(row)

        comfortIndex -= (1 * row['cloudiness'] / 100)

        # Учет влияния феномена на индекс комфорта
        comfortIndex -= 5*row['phenomenon']

        # Учет влияния видимости на индекс комфорта (можно дополнительно уточнить формулу)
        # Например, уменьшение индекса комфорта при низкой видимости
        if row['visibility'] < 5:  # Пример: если видимость менее 5 км
            comfortIndex -= 7

        # Учет влияния осадков на индекс комфорта
        comfortIndex -= (2 * row['sedges'])
        comfortIndeces.append(comfortIndex)

    coefs = []
    for comfortIndex in comfortIndeces:
        min_ci = min(comfortIndeces)
        max_ci = max(comfortIndeces)
        coef = (comfortIndex - min_ci) / (max_ci - min_ci)
        coefs.append(coef)
    df['CC'] = coefs

    return df

def main():
    pd.set_option('display.max_columns', None)
    df = pd.read_excel('./assets/valid_data.xlsx')

    coffeeshop1 = Coffeeshop(COFFEESHOP_DATA_PATH, 'Первая', 1)
    coffeeshop2 = Coffeeshop(COFFEESHOP_DATA_PATH, 'Вторая', 2)
    coffeeshop3 = Coffeeshop(COFFEESHOP_DATA_PATH, 'Третья', 3)

    df = df.rename(
        columns={'WW': 'phenomenon', 'Местное время в Санкт-Петербурге': 'date', 'T': 'temperature', 'U': 'humidity',
                 'Ff': 'windSpeed', 'N': 'cloudiness', 'VV': 'visibility', 'RRR': 'sedges'})
    convertObjectFieldToNumber(df)
    df = deleteNight(df)
    df = groupRowsByDay(df)
    df = addComfortCoefficientColumn(df)

    df = enrichWeatherTable(df, coffeeshop1.df)
    df = enrichWeatherTable(df, coffeeshop2.df)
    df = enrichWeatherTable(df, coffeeshop3.df)

    seasons = Seasons(df)

    coffeeshop1.autoArima()


main()
