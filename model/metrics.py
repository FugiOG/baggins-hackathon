from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np


class Metrics:

    @staticmethod
    def displayMetrics(real, predictions):
        print("Тест на стационарность:")
        dftest = adfuller(real - predictions, autolag='AIC')
        print("\tT-статистика = {:.3f}".format(dftest[0]))
        print("\tP-значение = {:.3f}".format(dftest[1]))
        print("Критические значения :")
        for k, v in dftest[4].items():
            print("\t{}: {} - Данные {} стационарны с вероятностью {}% процентов".format(k, v,
                                                                                         "не" if v < dftest[
                                                                                             0] else "",
                                                                                         100 - int(k[:-1])))

        # real=np.array(real[real.columns[0]].values)
        predictions = np.array(predictions)
        print('MAD:', round(abs(real - predictions).mean(), 4))
        print('MSE:', round(((real - predictions) ** 2).mean(), 4))
        print('MAPE:', round((abs(real - predictions) / real).mean(), 4))
        print('MPE:', round(((real - predictions) / real).mean(), 4))
        print('Стандартная ошибка:', round(((real - predictions) ** 2).mean() ** 0.5, 4))

        mae = mean_absolute_error(real, predictions)
        r2 = r2_score(real, predictions)

        print(f'Mean Absolute Error (MAE): {mae}')
        print(f'R-squared (R2 ): {r2}')
