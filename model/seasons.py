import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

seasons = ['winter', 'spring', 'summer', 'autumn']


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
        return df
