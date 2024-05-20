import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, r2_score
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller

from metrics import Metrics

from sklearn.ensemble import RandomForestRegressor


# from adtk.detector import ThresholdAD
# from adtk.visualization import plot

class Coffeeshop(Metrics):
    def __init__(self, filePath, pageName, id):
        df = pd.read_excel(filePath, sheet_name=pageName)

        df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')
        df['Дата'] = df['Дата'].dt.date

        df.rename(columns={'Дата': 'date', 'Кол-во заказов': f'ordersCount_{id}', 'Товарооборот': f'turnover_{id}'},
                  inplace=True)

        df = df.dropna(subset=[f'turnover_{id}']).reset_index()

        self._df = df
        self._id = id
        self.model = ExponentialSmoothing

        turnover = self._df[f'turnover_{self._id}']
        split_index = int(len(turnover) * 0.9)
        self.train_turnover = turnover[:split_index]
        self.test_turnover = turnover[split_index:]

        ordersCount = self._df[f'ordersCount_{id}']
        self.train_ordersCount = ordersCount[:split_index]
        self.test_ordersCount = ordersCount[split_index:

                            ]
    @property
    def df(self):
        return self._df

    def displayTurnoverFrequency(self):
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[f'turnover_{self._id}'], bins=30, edgecolor='black')
        plt.show()

    def autoArima(self):
        model = auto_arima(self.train_turnover, seasonal=False, stepwise=True, trace=False)
        model.fit(self.train_turnover)
        predictions = model.predict(n_periods=len(self.test_turnover))
        self.displayMetrics(self.test_turnover, predictions)
        return model

    def randomForest(self):
        model = RandomForestRegressor(n_estimators=500)
        model.fit(self.train_turnover)
        predictions = model.predict(self.test_turnover)
        self.displayMetrics(self.test_turnover, predictions)

    def autoArimaOrdersCount(self):
        model = auto_arima(self.train_ordersCount, seasonal=False, stepwise=True, trace=False)
        model.fit(self.train_ordersCount)
        predictions = model.predict(n_periods=len(self.test_ordersCount))
        self.displayMetrics(self.test_ordersCount, predictions)
        return model

    def randomForestOrdersCount(self):
        model = RandomForestRegressor(n_estimators=500)
        model.fit(self.train_ordersCount)
        predictions = model.predict(self.test_ordersCount)
        self.displayMetrics(self.test_ordersCount, predictions)
