import pandas as pd
from convertData import convertDataService
from seasons import Seasons
# import matplotlib.pyplot as plt
# from adtk.detector import ThresholdAD
# from adtk.visualization import plot
from coffeeshop import Coffeeshop

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
    print(coffeeshop3.df)

    df = enrichWeatherTable(df, coffeeshop1.df)
    df = enrichWeatherTable(df, coffeeshop2.df)
    df = enrichWeatherTable(df, coffeeshop3.df)

    print(df)

    seasons = Seasons(df)

    seasons.displayFirstsElement('winter')
    seasons.displayHeatMap('autumn')
    # trainingPredictTurnover(winter_df)

    coffeeshop1.displayTurnoverFrequency()
    print(coffeeshop3.df)
    coffeeshop3.displayTurnoverFrequency()

    # coffeeshop3.getAnomalies()

    # threshold_ad = ThresholdAD(high=24000, low=6500)
    # anomalies = threshold_ad.detect(coffeeshop3.dfWithoutCounts)
    # plot(coffeeshop3.df, anomaly=anomalies, ts_linewidth=1, ts_markersize=3, anomaly_markersize=5, anomaly_color='red', anomaly_tag="marker")


main()
