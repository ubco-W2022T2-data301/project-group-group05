import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt

sns.set_theme(style="ticks",
              font_scale=1.3, # This scales the fonts slightly higher
             )

df = pd.read_csv('../data/raw/Jan_2020_ontime.csv')
df.head()

#need to convert this to a python file and import the file


weekday = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}


def load_and_process_airplane(path):
    df1= (
        pd.read_csv(path)
        .loc[:,["DAY_OF_MONTH","DAY_OF_WEEK","CANCELLED","DEP_DEL15","ARR_DEL15"]]
        .rename(columns={"DEP_DEL15":"Departure_Delay","ARR_DEL15":"Arrival_Delay"}) 
    )
    
    df2=(
        df1
        .assign(CANCELLED=df1['CANCELLED'].astype(bool))
        .assign(Departure_Delay=df1['Departure_Delay'].astype(bool))
        .assign(Arrival_Delay=df1['Arrival_Delay'].astype(bool))
        
        
    )
    return df2

def graph_set_1(df2):
    df2_1=df2
    df3=(df2
        .drop(columns=["DAY_OF_WEEK"])
        .groupby("DAY_OF_MONTH")[["CANCELLED","Departure_Delay","Arrival_Delay"]]
        .agg({
            "CANCELLED": "sum",
            "Departure_Delay": "sum",
            "Arrival_Delay": "sum",
            })
               
    )
    df3["total_flights"]=df2_1["DAY_OF_MONTH"].value_counts()
    df4=(df3
        .reset_index()
        .assign(perctentage_of_flights_cancelled=lambda x:x["CANCELLED"]/x["total_flights"]*100)
        .assign(perctentage_of_flights_dealyed_on_departure=lambda x:x["Departure_Delay"]/x["total_flights"]*100)
        .assign(perctentage_of_flights_dealyed_on_arrival=lambda x:x["Arrival_Delay"]/x["total_flights"]*100)
    )
    return df4

def percent(df4):
    df5=(df4
         .drop(["CANCELLED","Departure_Delay","Arrival_Delay","total_flights"],axis=1)    
    )
    return df5

def weekly(df2):
    df2_1=df2
    df6=(df2
        .drop(columns=["DAY_OF_MONTH"])
        .groupby("DAY_OF_WEEK")[["CANCELLED","Departure_Delay","Arrival_Delay"]]
        .agg({
            "CANCELLED": "sum",
            "Departure_Delay": "sum",
            "Arrival_Delay": "sum",
        })  
    )
    df6["total_flights"]=df2_1["DAY_OF_WEEK"].value_counts()
    df7=(df6
        .reset_index()
        .assign(perctentage_of_flights_cancelled=lambda x:x["CANCELLED"]/x["total_flights"]*100)
        .assign(perctentage_of_flights_dealyed_on_departure=lambda x:x["Departure_Delay"]/x["total_flights"]*100)
        .assign(perctentage_of_flights_dealyed_on_arrival=lambda x:x["Arrival_Delay"]/x["total_flights"]*100)
        .drop(["CANCELLED","Departure_Delay","Arrival_Delay","total_flights"],axis=1)
        
    )
    df7["DAY_OF_WEEK"]=df7["DAY_OF_WEEK"].map(weekday)
    print(df7)
    return df7
def weeklyadd(df7):
    
    df8=df7.melt(id_vars=["DAY_OF_WEEK"], var_name="days",value_name="flights %")
    return df8

# data set for covid
def covid_load(path):
    dfc1 = (pd.read_csv(path)
        .query('Date_reported >= "2020-01-01" & Date_reported < "2020-02-01"')
        .assign(Country = lambda x: np.where(x.Country_code == 'US', 'United States', x.Country))
        .drop(columns=['WHO_region'])
           
       )
    dfc1["Date_reported"]=pd.to_datetime(dfc1["Date_reported"])
    dfc1["Date_reported"]=dfc1["Date_reported"].dt.day
    return dfc1
def data_process_1(dfc1):
    dfc2=(dfc1
        .groupby("Date_reported")[["New_cases","New_deaths"]]
        .agg({
            "New_cases": "sum",
            "New_deaths": "sum",
        })
        .reset_index()
        )
    
    return dfc2

def data_process_2(dfc1):
    dfc3=(dfc1
        .groupby("Date_reported")[["Cumulative_cases","Cumulative_deaths"]]
        .agg({
            "Cumulative_cases": "sum",
            "Cumulative_deaths": "sum",
        })
        .reset_index()
        )
    return dfc3

df2=load_and_process_airplane('../data/raw/Jan_2020_ontime.csv')
df3=graph_set_1(df2)
df3.head()


plt.figure(figsize=(10, 8))
ax_daily_arrival=sns.barplot(data=df3, x="DAY_OF_MONTH", y="Arrival_Delay")
ax_daily_arrival.set(title="Delays on arrivals")

plt.figure(figsize=(10, 8))
ax_daily_departure=sns.barplot(data=df3, x="DAY_OF_MONTH", y="Departure_Delay")
ax_daily_departure.set(title="Delays on departures")

plt.figure(figsize=(10, 8))
ax_daily_cancelled=sns.barplot(df3, x="DAY_OF_MONTH", y="CANCELLED")
ax_daily_cancelled.set(title="Cancelled flights")

df_c1=covid_load('../data/raw/WHO-COVID-19-global-data.csv')
df_c2=data_process_1(df_c1)
df_c2.head()

plt.figure(figsize=(10, 8))
ax_daily_cases=sns.barplot(df_c2, x="Date_reported", y="New_cases")
ax_daily_cases.set(title="Covid cases in January 2020")

ax_daily_deaths=sns.barplot(df_c2, x="Date_reported", y="New_deaths")
ax_daily_deaths.set(title="Covid deaths in January 2020")

df4=percent(df3)
plt.figure(figsize=(10, 8))
ax_daily_plot2=sns.lineplot(data= df4.set_index("DAY_OF_MONTH"))
ax_daily_plot2.set(title="Flights adjusted during January 2020 %", ylabel="Number of flights %", xlim=(0,35),ylim=(0,40))
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper right',fontsize="small")
plt.show

df_c3=data_process_2(df_c1)
ax_cumulative_cases=sns.lineplot(data=df_c3,x="Date_reported",y="Cumulative_cases")
ax_cumulative_cases.set(title="Cumulative cases in January 2020")

ax_cumulative_deaths=sns.lineplot(data=df_c3,x="Date_reported",y="Cumulative_deaths")
ax_cumulative_deaths.set(title="Cumulative deaths in January 2020")



df5=weekly(df2)
df6=weeklyadd(df5)
sns.set(rc={"figure.figsize":(10,8)})
ax_day_plot2=sns.barplot(data=df6, x ="DAY_OF_WEEK",y="flights %" , hue="days")
ax_day_plot2.set(title="Flight delays in January 2020 sorted by day")

#df3.to_csv('../data/processed/aakash/percentages.csv', index=False)
#df_c2.to_csv('../data/processed/aakash/covid.csv', index=False)
#df4.to_csv('../data/processed/aakash/percentages2.csv', index=False)
#df_c3.to_csv('../data/processed/aakash/covid2.csv', index=False)
df5.to_csv('../data/processed/aakash/weekly.csv', index=False)

# data set for covid
def covid_load(path):
    dfc1 = (pd.read_csv(path)
        .query('Date_reported >= "2020-01-01" & Date_reported < "2020-02-01"')
        .assign(Country = lambda x: np.where(x.Country_code == 'US', 'United States', x.Country))
        .drop(columns=['WHO_region'])
           
       )
    dfc1["Date_reported"]=pd.to_datetime(dfc1["Date_reported"])
    dfc1["Date_reported"]=dfc1["Date_reported"].dt.day
    return dfc1
def data_process_1(dfc1):
    dfc2=(dfc1
        .groupby("Date_reported")[["New_cases","New_deaths"]]
        .agg({
            "New_cases": "sum",
            "New_deaths": "sum",
        })
        .reset_index()
        )
    
    return dfc2

def data_process_2(dfc1):
    dfc3=(dfc1
        .groupby("Date_reported")[["Cumulative_cases","Cumulative_deaths"]]
        .agg({
            "Cumulative_cases": "sum",
            "Cumulative_deaths": "sum",
        })
        .reset_index()
        )
    return dfc3


