import pandas as pd
from convertData import convertDataService
import matplotlib.pyplot as plt
import seaborn as sns
from training import trainingPredictTurnover

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


def enrichWeatherTable(df: pd.DataFrame):
    file_path = './assets/data.xlsx'
    store1_df = pd.read_excel(file_path, sheet_name='Первая')
    store2_df = pd.read_excel(file_path, sheet_name='Вторая')
    store3_df = pd.read_excel(file_path, sheet_name='Третья')

    store1_df['Дата'] = pd.to_datetime(store1_df['Дата'], format='%d.%m.%Y')
    store2_df['Дата'] = pd.to_datetime(store2_df['Дата'], format='%d.%м.%Y')
    store3_df['Дата'] = pd.to_datetime(store3_df['Дата'], format='%d.%m.%Y')

    store1_df['Дата'] = store1_df['Дата'].dt.date
    store2_df['Дата'] = store2_df['Дата'].dt.date
    store3_df['Дата'] = store3_df['Дата'].dt.date

    store1_df.rename(columns={'Дата': 'date', 'Кол-во заказов': 'ordersCount1', 'Товарооборот': 'turnover1'},
                     inplace=True)
    store2_df.rename(columns={'Дата': 'date', 'Кол-во заказов': 'ordersCount2', 'Товарооборот': 'turnover2'},
                     inplace=True)
    store3_df.rename(columns={'Дата': 'date', 'Кол-во заказов': 'ordersCount3', 'Товарооборот': 'turnover3'},
                     inplace=True)

    merged_df = df.merge(store1_df, on='date', how='left') \
        .merge(store2_df, on='date', how='left') \
        .merge(store3_df, on='date', how='left')

    return merged_df

# Определение функции для определения сезона
def get_season(date):
    if date.month in [12, 1, 2, 3]:
        return 'Winter'
    elif date.month in [4, 5]:
        return 'Spring'
    elif date.month in [6, 7, 8]:
        return 'Summer'
    elif date.month in [9, 10, 11]:
        return 'Autumn'

def main():
    pd.set_option('display.max_columns', None)
    df = pd.read_excel('./assets/valid_data.xlsx')
    df = df.rename(
        columns={'WW': 'phenomenon', 'Местное время в Санкт-Петербурге': 'date', 'T': 'temperature', 'U': 'humidity',
                 'Ff': 'windSpeed', 'N': 'cloudiness', 'VV': 'visibility', 'RRR': 'sedges'})
    convertObjectFieldToNumber(df)
    df = deleteNight(df)
    df = groupRowsByDay(df)
    df = enrichWeatherTable(df)

    df['season'] = df['date'].apply(get_season)
    winter_df = df[df['season'] == 'Winter']
    sprint_df = df[df['season'] == 'Spring']
    winter_df = winter_df.drop(columns=['date', 'season'])
    # plt.figure(figsize=(14, 12))
    # sns.heatmap(df.corr(), annot=True, annot_kws={"size": 14})
    # sns.set_style("white")
    # plt.xticks(rotation=90, fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.show()
    # print(df.head(5))
    winter_df = winter_df.drop(columns=['turnover2', 'turnover3', 'ordersCount1', 'ordersCount2', 'ordersCount3'])
    winter_df = winter_df.dropna(subset=['turnover1'])
    # winter = df[df['date'].dt.month > 11].reset_index()
    trainingPredictTurnover(winter_df)

main()
