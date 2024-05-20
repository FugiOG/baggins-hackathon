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

def addComfortCoefficientColumn(df: pd.DataFrame):
    comfortIndeces = []
    phenomenons = []
    for index, row in df.iterrows():
        comfortIndex = calculateComfortIndex(row)
        comfortIndeces.append(comfortIndex)
        phenomenons.append(row['phenomenon'])

    coefs = []
    min_ci = min(comfortIndeces)
    max_ci = max(comfortIndeces)

    for i in range(len(comfortIndeces)):
        coef = (comfortIndeces[i] - min_ci) / (max_ci - min_ci)
        if phenomenons[i] > 0:
            coef /= 0.85 + phenomenons[i]
        coefs.append(coef)
    df['CC'] = coefs

    return df

def getPredict(coeffs, coffeeshop, start_date = '2023-03-01', end_date = '2023-03-30'):
    model = coffeeshop.autoArima()
    pr_df = model.predict(n_periods=30).to_frame()

    date_range = pd.date_range(start=start_date, end=end_date)
    pr_df.insert(0, 'date', date_range.tolist())
    pr_df['CC'] = coeffs
    pr_df = pr_df.rename(columns={0: 'turnover'})

    model = coffeeshop.autoArimaOrdersCount()
    pr_df['ordersCount'] = model.predict(n_periods=30).to_frame()[0].tolist()

    pr_df['turnover'] = (pr_df['turnover'] * (0.5 + pr_df['CC'])).round().astype(int)
    pr_df['ordersCount'] = (pr_df['ordersCount'] * (0.5 + pr_df['CC'])).round().astype(int)

    pr_df = pr_df.reset_index().drop(columns=['CC', 'index'])
    return pr_df

def displayPlot(df: pd.DataFrame):
    plt.figure(figsize=(14, 7))

    # График товарооборота
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['turnover'], marker='o', linestyle='-', color='blue')
    plt.title('Товарооборот по датам')
    plt.xlabel('Дата')
    plt.ylabel('Товарооборот')
    plt.xticks(rotation=45)

    # График количества заказов
    plt.subplot(2, 1, 2)
    plt.plot(df['date'], df['ordersCount'], marker='o', linestyle='-', color='green')
    plt.title('Количество заказов по датам')
    plt.xlabel('Дата')
    plt.ylabel('Количество заказов')
    plt.xticks(rotation=45)

    # Автоматическая подгонка макета
    plt.tight_layout()
    plt.show()

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

    displayCC(df)
    #df = enrichWeatherTable(df, coffeeshop1.df)
    #df.to_excel("output.xlsx")
    #df = enrichWeatherTable(df, coffeeshop2.df)
    #df = enrichWeatherTable(df, coffeeshop3.df)

    coeffs = df[(df['date'] >= pd.to_datetime('2023-03-01')) & (df['date'] <= pd.to_datetime('2023-03-30'))]['CC'].tolist()
    print(df)

    #df = df.dropna(subset=['turnover_1', 'turnover_2', 'turnover_3']).reset_index()
    #seasons = Seasons(df)
    # seasons.dfs['winter'].LSTMModel()

    # seasons.createSeasonDf()

    pr_df = getPredict(coeffs=coeffs, coffeeshop=coffeeshop1)
    displayPlot(pr_df)
    # coffeeshop1.randomForest()


main()
