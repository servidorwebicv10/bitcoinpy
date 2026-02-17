import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend para generar gráficos sin GUI
import matplotlib.pyplot as plt
from flask import Flask, render_template
import numpy as np
from pygam import LinearGAM, s
from sklearn.metrics import mean_squared_error

app = Flask(__name__)

# Gráfica 1: Precio de cierre desde 2020 hasta la actualidad
def get_plt():
    df = pd.read_csv("bitcoin.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df_filt = df[df["Date"] >= "2020-01-01"].sort_values(by="Date")

    plt.figure(figsize=(12, 6))
    plt.plot(df_filt["Date"], df_filt["Close"], label="Precio de cierre", color="orange")
    plt.title("Precio del Bitcoin (Cierre) desde el 2020 hasta la actualidad")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (USD)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return plt

# Gráfica 2: Varianza diaria (High - Low)
def get_plt2():
    df = pd.read_csv("bitcoin.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[df["Date"] >= "2024-07-31"]
    df["Varianza"] = df["High"] - df["Low"]
    df = df.sort_values(by="Date")

    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Varianza"], color='purple', label="Varianza diaria (High - Low)")
    plt.title("Varianza diaria entre High y Low del Bitcoin (2020 - 2025)")
    plt.xlabel("Fecha")
    plt.ylabel("Varianza en USD")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return plt

# Gráfica 3: Predicción futura de High y Low con GAM
def get_plt3():
    df = pd.read_csv("bitcoin.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Days'] = (df['Date'] - df['Date'].min()).dt.days

    X = df[['Days', 'Volume']].values
    y_high = df['High'].values
    y_low = df['Low'].values

    gam_high = LinearGAM(s(0) + s(1)).gridsearch(X, y_high)
    gam_low = LinearGAM(s(0) + s(1)).gridsearch(X, y_low)

    last_day = df['Days'].max()
    last_volume = df['Volume'].iloc[-1]

    future_days = np.arange(last_day + 1, last_day + 99)
    future_volume = np.full_like(future_days, fill_value=last_volume)
    future_X = np.column_stack((future_days, future_volume))

    pred_high = gam_high.predict(future_X)
    pred_low = gam_low.predict(future_X)

    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], y_high, label='High histórico', color='orange', alpha=0.6)
    plt.plot(df['Date'], y_low, label='Low histórico', color='blue', alpha=0.6)

    future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=98)
    plt.plot(future_dates, pred_high, label='Predicción High', color='red', linestyle='--')
    plt.plot(future_dates, pred_low, label='Predicción Low', color='green', linestyle='--')

    plt.title("Predicción futura de High y Low con GAM")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Opcional: imprimir RMSE (puedes comentar si no quieres que se vea en consola)
    pred_high_actual = gam_high.predict(X)
    pred_low_actual = gam_low.predict(X)
    rmse_high = mean_squared_error(y_high, pred_high_actual) ** 0.5
    rmse_low = mean_squared_error(y_low, pred_low_actual) ** 0.5

    print(f"RMSE High: {rmse_high:.2f}")
    print(f"RMSE Low: {rmse_low:.2f}")

    return plt

#Grafica 4 del Volumen
def get_plt4():
    df = pd.read_csv('bitcoin.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month_Year'] = df['Date'].dt.strftime('%Y-%m')
    print(df.head())
    print(df.info())
    monthly_volume = df.groupby('Month_Year')['Volume'].sum()
    print(monthly_volume.head())
    month_max_volume = monthly_volume.idxmax()  
    max_monthly_volume = monthly_volume.max()  
    print(f"El mes con el volumen más alto es: {month_max_volume} con un volumen de: {max_monthly_volume}")
    df_highest_volume_month = df[df['Month_Year'] == month_max_volume]
    print(df_highest_volume_month.head())
    df_top_30_volume_days = df_highest_volume_month.sort_values(by='Volume', ascending=False).head(30)
    print(df_top_30_volume_days.head())
    plt.figure(figsize=(12, 6))
    plt.bar(df_top_30_volume_days['Date'], df_top_30_volume_days['Volume'], color="orange")
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.title('Top 30 Days with Highest Volume in the Month with Highest Volume (Bar Chart)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/grafica1')
def show_plot1():
    if not os.path.exists('static'):
        os.makedirs('static')
    plot1 = get_plt()
    plot1.savefig(os.path.join('static', 'plot1.png'))
    plot1.close()
    return render_template('grafica1.html')  # este HTML debe mostrar la imagen

@app.route('/grafica2')
def show_plot2():
    if not os.path.exists('static'):
        os.makedirs('static')
    plot2 = get_plt2()
    plot2.savefig(os.path.join('static', 'plot2.png'))
    plot2.close()
    return render_template('grafica2.html')

@app.route('/grafica3')
def show_plot3():
    if not os.path.exists('static'):
        os.makedirs('static')
    plot3 = get_plt3()
    plot3.savefig(os.path.join('static', 'plot3.png'))
    plot3.close()
    return render_template('grafica3.html')

@app.route('/grafica4')
def show_plot4():
    if not os.path.exists('static'):
        os.makedirs('static')
    plot4 = get_plt4()
    plot4.savefig(os.path.join('static', 'plot4.png'))
    plot4.close()
    return render_template('grafica4.html')


if __name__ == '__main__':
    app.run(debug=True)
