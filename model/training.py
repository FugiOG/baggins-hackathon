import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor


def trainingPredictTurnover(df: pd.DataFrame):
    turnover = df["turnover1"]
    feature = df[["temperature"]]
    # feature = df.drop(["turnover1"], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(feature, turnover, test_size=0.2, random_state=10)

    # Создание модели
    model = LinearRegression()

    # Обучение модели
    model.fit(X_train, y_train)

    # Предсказание на тестовой выборке
    y_pred = model.predict(X_test)

    # Оценка качества модели
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'Mean Squared Error: {mse}')
    print(f'R^2 Score: {r2}')

    print('Training data', model.score(X_train, y_train))
    print('Testing data', model.score(X_test, y_test))
    # regr = LogisticRegression(solver='lbfgs', max_iter=10000)
    # regr = HistGradientBoostingRegressor()
    # regr.fit(X_train, y_train)
    # print("x_test", X_test)
    # print("y_test", y_test)
    # print("train score:", regr.score(X_train, y_train))
    # print("test score:", regr.score(X_test, y_test))
    # print('Intercept:', regr.intercept_)
