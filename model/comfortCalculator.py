import math
import matplotlib.pyplot as plt


def heat_index(temperature: float, humidity: float):
    """
    Рассчитывает температурно-влажностный индекс (Heat Index).
    Параметры:
    temperature (°C) - температура воздуха
    humidity (%) - относительная влажность

    Возвращает:
    Heat Index (°C)
    """
    hi = temperature - ((0.55 - 0.0055 * humidity) * (temperature - 14.5))
    return hi


def wind_chill(temperature: float, wind_speed: float):
    """
    Рассчитывает индекс охлаждения ветром (Wind Chill Index).
    Параметры:
    temperature (°C) - температура воздуха
    wind_speed (км/ч) - скорость ветра

    Возвращает:
    Wind Chill Index (°C)
    """
    wci = 13.12 + 0.6215 * temperature - 11.37 * math.pow(wind_speed, 0.16) + 0.3965 * temperature * math.pow(
        wind_speed, 0.16)
    return wci


def calculateComfortIndex(row):
    """
    Рассчитывает общий индекс комфорта.
    Параметры:
    temperature (°C) - температура воздуха
    humidity (%) - относительная влажность
    wind_speed (км/ч) - скорость ветра

    Возвращает:
    Comfort Index (°C)
    """
    temperature = row['temperature']
    humidity = row['humidity']
    wind_speed = row['windSpeed']
    hi = heat_index(temperature, humidity)
    wci = wind_chill(temperature, wind_speed)
    ci = (hi + wci) / 2
    return ci


def displayCC(df):
    dates = df['date']  # Предполагается, что столбец 'date' содержит даты в формате datetime
    comfort_indices = df['CC']

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.bar(dates, comfort_indices, color='skyblue', alpha=0.7)  # Создание столбчатой диаграммы
    plt.xlabel('Дата')
    plt.ylabel('Кэф комфорта')
    plt.title('Кэф по датам')
    plt.xticks(rotation=45)  # Поворот меток по оси X на 45 градусов для лучшей читаемости
    plt.tight_layout()  # Автоматическое регулирование макета графика
    plt.show()

    """
    Градация индекса комфорта
    < 0°C: Очень холодно
    0°C - 10°C: Холодно
    10°C - 18°C: Прохладно
    18°C - 24°C: Комфортно
    24°C - 27°C: Тепло
    27°C - 30°C: Немного жарко
    30°C - 35°C: Жарко
    35°C - 40°C: Очень жарко
    > 40°C: Экстремальная жара
    """
