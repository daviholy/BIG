import pandas as pd
import matplotlib.pyplot as plt
import pyspark.pandas as ps
from pyspark.sql import SparkSession, Row
from datetime import date, datetime
import pyspark.pandas as ps

session = SparkSession.builder.remote("sc://localhost:15002").getOrCreate() # type: ignore
def load_data(name):
    df = pd.read_csv(f'Data/{name}.csv', skiprows=24, encoding='latin2',delimiter=';', names=['year', 'month', 'day', f'temperature_{name}', 'flag'], header=0)
    df[f"temperature_{name}"] = df[f"temperature_{name}"].str.replace(",",".").astype(float)
    df['date'] = ps.to_datetime(df[["year", "month", "day"]])
    # df = df.set_index('date')
    df = session.createDataFrame(df)

    # df[f'temperature_{name}'] = df[f'temperature_{name}'].replace(',','.').astype(float)

    return df[[f"temperature_{name}","date"]]


def main():

    df_d = load_data('Doksany')
    df_c = load_data('Churanov')

    df = df_d.join(df_c,"date")
    df = df.pandas_api()


    a = df.resample('Y', on=df["date"]).mean().sort_index().plot.line()
    # a = df.groupby(df.date.dtA.month).mean().plot.line(y=["temperature_Doksany","temperature_Churanov"])
    a.show()
    # plt.show()

    # TODO regresy řád 1
    # TODO vyhlazení plovoucí průměry











if __name__ == '__main__':
    main()

