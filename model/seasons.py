import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from metrics import Metrics

from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense

seasons = ['winter', 'spring', 'summer', 'autumn']


class Season(Metrics):
    def __init__(self, df: pd.DataFrame):
        df = df.drop(columns=['ordersCount_2', 'ordersCount_3', 'turnover_2', 'turnover_3', 'ordersCount_1', 'date'])
        self._df = df
        target = self._df['turnover_1']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self._df.drop(columns=['turnover_1']), target, test_size=0.1, shuffle=False)
        print(self.X_train, self.y_train)

    def randomForest(self):
        model = RandomForestRegressor(n_estimators=100)
        model.fit(self.X_train, self.y_train)
        predictions = model.predict(self.X_test)
        self.displayMetrics(self.y_test, predictions)

    def LSTMModel(self):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(60, 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(self.X_train, self.y_train, batch_size=1, epochs=1)

        predictions = model.predict(self.X_test)
        self.displayMetrics(self.y_test, predictions)
        # predictions = scaler.inverse_transform(predictions)


class Seasons:
    def __init__(self, df: pd.DataFrame):
        df['season'] = df['date'].apply(self.get_season)
        self.dfs = {}
        for season in seasons:
            self.dfs[season] = self.createSeasonDf(df, season)

    def displayHeatMap(self, season: str):
        plt.figure(figsize=(14, 12))
        df = self.dfs[season].drop(columns=['date'])
        sns.heatmap(df.corr(), annot=True, annot_kws={"size": 14})
        sns.set_style("white")
        plt.xticks(rotation=90, fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

    def displayFirstsElement(self, season: str):
        print(self.dfs[season].head(10))

    @staticmethod
    def get_season(date):
        if date.month in [12, 1, 2, 3]:
            return 'winter'
        elif date.month in [4, 5]:
            return 'spring'
        elif date.month in [6, 7, 8]:
            return 'summer'
        elif date.month in [9, 10, 11]:
            return 'autumn'

    @staticmethod
    def createSeasonDf(df: pd.DataFrame, season: str):
        df = df[df['season'] == season]
        df = df.drop(['season'], axis=1)
        return Season(df)
