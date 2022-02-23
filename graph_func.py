import matplotlib.pyplot as plt
import pandas as pd


def plot_trajectory():
    data = pd.read_csv(r'C:\Users\rafka\Desktop\Сервер\log\data1.csv', sep=';', names=range(9))
    plt.plot(data[1], data[0])
    plt.xlim([-155, 155]), plt.ylim([-155, 155])
    plt.show()
