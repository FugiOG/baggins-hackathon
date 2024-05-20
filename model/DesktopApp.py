import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

from model.coffeeshop import Coffeeshop
import utils as utl


class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")

        self.weather_file = None
        self.data_file = None

        self.select_weather_button = tk.Button(root, text="Select Weather File", command=self.select_weather_file)
        self.select_weather_button.pack(pady=10)

        self.select_data_button = tk.Button(root, text="Select Data File", command=self.select_data_file)
        self.select_data_button.pack(pady=10)

        self.plot_button = tk.Button(root, text="Plot Data", command=self.plot_data)
        self.plot_button.pack(pady=10)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)

    def select_weather_file(self):
        self.weather_file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.weather_file:
            self.status_label.config(text=f"Selected weather file: {self.weather_file}")

    def select_data_file(self):
        self.data_file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.data_file:
            self.status_label.config(text=f"Selected data file: {self.data_file}")

    def plot_data(self):
        if not self.weather_file or not self.data_file:
            self.status_label.config(text="Please select both files before plotting.")
            return

        try:
            pd.set_option('display.max_columns', None)

            df = pd.read_excel(self.weather_file)

            coffeeshop1 = Coffeeshop(self.data_file, 'Первая', 1)
            coffeeshop2 = Coffeeshop(self.data_file, 'Вторая', 2)
            coffeeshop3 = Coffeeshop(self.data_file, 'Третья', 3)
            df = df.rename(
                columns={'WW': 'phenomenon', 'Местное время в Санкт-Петербурге': 'date', 'T': 'temperature',
                         'U': 'humidity',
                         'Ff': 'windSpeed', 'N': 'cloudiness', 'VV': 'visibility', 'RRR': 'sedges'})
            utl.convertObjectFieldToNumber(df)
            df = utl.deleteNight(df)
            df = utl.groupRowsByDay(df)
            df = utl.addComfortCoefficientColumn(df)

            coeffs = df[(df['date'] >= pd.to_datetime('2023-03-01')) & (df['date'] <= pd.to_datetime('2023-03-30'))][
                'CC'].tolist()

            pr_df = utl.getPredict(coeffs=coeffs, coffeeshop=coffeeshop1)
            pr_df2 = utl.getPredict(coeffs=coeffs, coffeeshop=coffeeshop2)
            pr_df3 = utl.getPredict(coeffs=coeffs, coffeeshop=coffeeshop3)
            utl.displayPlot(pr_df)
            utl.displayPlot(pr_df2)
            utl.displayPlot(pr_df3)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()
