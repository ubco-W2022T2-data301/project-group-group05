import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt

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

