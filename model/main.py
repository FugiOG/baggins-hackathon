import pandas as pd
from convertData import convertDataService


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

    store1_df.rename(columns={'Дата': 'date', 'Кол-во заказов': 'ordersCount1', 'Товарооборот': 'turnover1'}, inplace=True)
    store2_df.rename(columns={'Дата': 'date', 'Кол-во заказов': 'ordersCount2', 'Товарооборот': 'turnover2'}, inplace=True)
    store3_df.rename(columns={'Дата': 'date', 'Кол-во заказов': 'ordersCount3  ', 'Товарооборот': 'turnover3'}, inplace=True)

    merged_df = df.merge(store1_df, on='date', how='left') \
        .merge(store2_df, on='date', how='left') \
        .merge(store3_df, on='date', how='left')

    return merged_df

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
    print(df.head(5))


main()
