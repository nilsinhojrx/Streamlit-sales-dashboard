import pandas as pd
import plotly.express as px

# Convert month number into its names:
def translate_month(num:int):
    month_names = {1:"Jan",
              2:"Feb",
              3:"Mar",
              4:"April",
              5:"May",
              6:"Jun",
              7:"Jul",
              8:"Aug",
              9:"Sep",
             10:"Oct",
             11:"Nov",
             12:"Dec"}
    return month_names[num]

# Load excel file
def loadData(path):
    df = pd.read_excel(
        io=path,
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000
    )
    df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    df["Date"] = pd.to_datetime(df["Date"], format= "%d/%m/%Y")
    df["Month"] = pd.to_datetime(df["Date"], format= "%d/%m/%Y").dt.month
    df["Month"] = df["Month"].apply(translate_month)
    df.drop("Time", axis=1, inplace=True)
    return df

# Bar Chart: sales by Product Line
def productline_sales(data):
    fig = px.bar(
        data,
        x="Total",
        y=data.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence = ["#0083B8"]*len(data),
        template="plotly_white",
    )
    return fig

# Bar Chart: Sales per Hour
def hourly_sales(data):
    fig = px.bar(
        data,
        x=data.index,
        y="Total",
        orientation="v",
        title="<b>Sales by Hour</b>",
        color_discrete_sequence = ["#0083B8"]*len(data),
        template="plotly_white",
    )
    return fig

if __name__ == "__main__":
    df=loadData("supermarkt_sales.xlsx")
    print(df)

'''
df = pd.read_excel(io=path, engine="openpyxl", sheet_name="Sales", skiprows=3, usecols="B:R", nrows=1000)
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
'''
