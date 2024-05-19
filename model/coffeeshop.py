import pandas as pd
import matplotlib.pyplot as plt
# from adtk.detector import ThresholdAD
# from adtk.visualization import plot

class Coffeeshop:
    def __init__(self, filePath, pageName, id):
        df = pd.read_excel(filePath, sheet_name=pageName)

        df['Дата'] = pd.to_datetime(df['Дата'], format='%Y-%m-%d')
        df['Дата'] = df['Дата'].dt.date

        df.set_index(pd.DatetimeIndex(df['Дата']), inplace=True)

        df.rename(columns={'Дата': 'date', 'Кол-во заказов': f'ordersCount_{id}', 'Товарооборот': f'turnover_{id}'},
                         inplace=True)

        self._df = df
        self._id = id

    @property
    def df(self):
        return self._df

    # def getAnomalies(self):
    #     sns.set_style('whitegrid')
    #     df = self._df.drop(columns=['date', f'ordersCount_{self._id}'])
    #     df = df.dropna(subset=[f'turnover_{self._id}'])
    #     threshold_ad = ThresholdAD(high=24000, low=6500)
    #     anomalies = threshold_ad.detect(df)
    #     print(anomalies)
    #
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(df, label='Data')
    #     plt.scatter(anomalies.index, anomalies[f'turnover_{self._id}'], color='red', label='Anomalies')
    #     plt.title('Data with Anomalies')
    #     plt.xlabel('Index')
    #     plt.ylabel('Value')
    #     plt.legend()
    #     plt.show()

    def displayTurnoverFrequency(self):
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[f'turnover_{self._id}'], bins=30, edgecolor='black')
        plt.show()