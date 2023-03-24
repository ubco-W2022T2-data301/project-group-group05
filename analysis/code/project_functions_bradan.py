import pandas as pd
import numpy as np

def process_time(df: pd.DataFrame, time_prefix: str):
    ''' Jankily convert times to datetimes for the flights '''
    # Estimated departure times
    df['Departure time (min)'] = pd.to_datetime(time_prefix+df['DAY_OF_MONTH'].astype(str)+' '+df['DEP_TIME_BLK'].str[:4], utc=True)
    df['Departure time (max)'] = pd.to_datetime(time_prefix+df['DAY_OF_MONTH'].astype(str)+' '+df['DEP_TIME_BLK'].str[-4:], utc=True)
    df.loc[df['Departure time (max)'] < df['Departure time (min)'], 'Departure time (max)'] += pd.DateOffset(days=1)
    # Actual departure time
    dt = df['DEP_TIME'].fillna(0).astype(int).astype(str).str.pad(4,'left','0')
    dt.loc[dt == '2400'] = '0000'
    df['Departure time'] = pd.to_datetime(time_prefix+df['DAY_OF_MONTH'].astype(str)+' '+dt, utc=True)
    # Actual arrival time
    at = df['ARR_TIME'].fillna(0).astype(int).astype(str).str.pad(4,'left','0')
    at.loc[at == '2400'] = '0000'
    df['Arrival time'] = pd.to_datetime(time_prefix+df['DAY_OF_MONTH'].astype(str)+' '+at, utc=True)
    # Correct for time wraparound and NA
    #df.loc[df['Departure time'] < df['Departure time (min)'], 'Departure time'] += pd.DateOffset(days=1)
    df.loc[df['Arrival time'] < df['Departure time (min)'], 'Arrival time'] += pd.DateOffset(days=1)
    df.loc[df['Arrival time'] < df['Departure time'], 'Arrival time'] += pd.DateOffset(days=1)
    df.loc[df['DEP_TIME'].isna(), 'Departure time'] = np.nan
    df.loc[df['ARR_TIME'].isna(), 'Arrival time'] = np.nan
    return df

def load_who_data(start: str, end: str):
    return (pd.read_csv('../data/raw/WHO-COVID-19-global-data.csv')
       .query('Date_reported >= "'+start+'" & Date_reported < "'+end+'"')
       .assign(Country = lambda x: np.where(x.Country_code == 'MP', 'Northern Mariana Islands', x.Country))
       .assign(Country = lambda x: np.where(x.Country_code == 'US', 'United States', x.Country))
       .assign(Country = lambda x: np.where(x.Country_code == 'VI', 'Virgin Islands', x.Country))
       .assign(Date_reported = lambda x: pd.to_datetime(x.Date_reported, utc=True))
       .drop(columns=['Country_code', 'WHO_region'])
       .rename(columns={'Date_reported': 'Date reported',
               'New_cases': 'New cases',
               'Cumulative_cases': 'Cumulative cases',
               'New_deaths': 'New deaths',
               'Cumulative_deaths': 'Cumulative deaths'})
       .set_index(['Date reported', 'Country'])
      )

def load_country_data():
    return (pd.read_csv(airports, header=None)
            .rename(columns={3: 'Country', 4: 'IATA'})
            .drop(columns=[0, 1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13])
            .assign(IATA = lambda x: np.where(x.IATA == "\\N", np.nan, x.IATA))
            .dropna(subset='IATA')
           )

def load_and_process(flights: str, airports: str, who: str):
    ''' Big gross processing funcion '''
    # Import airports
    airports = load_country_data()

    # Import flights
    flights = (process_time(pd.read_csv(flights), '2020-2-')
               .assign(departure_delay = lambda x: (x['Departure time'] - x['Departure time (max)']))
               .assign(departure_delay = lambda x: np.where(x.departure_delay < np.timedelta64(0), np.timedelta64(0), x.departure_delay))
               .drop(columns=['Unnamed: 21', 'DAY_OF_MONTH', 'DAY_OF_WEEK','OP_UNIQUE_CARRIER',
                            'OP_CARRIER_AIRLINE_ID', 'OP_CARRIER', 'OP_CARRIER_FL_NUM', 'ORIGIN_AIRPORT_ID',
                            'ORIGIN_AIRPORT_SEQ_ID', 'DEST_AIRPORT_ID', 'DEST_AIRPORT_SEQ_ID', 'TAIL_NUM',
                            'DEP_TIME', 'DEP_TIME_BLK', 'ARR_TIME'])
               .assign(DEP_DEL15 = lambda x: (x.DEP_DEL15 == 1))
               .assign(ARR_DEL15 = lambda x: (x.ARR_DEL15 == 1))
               .assign(CANCELLED = lambda x: (x.CANCELLED == 1))
               .assign(DIVERTED = lambda x: (x.DIVERTED == 1))
               .rename(columns={'ORIGIN': 'Origin IATA',
                            'DEST': 'Destination IATA',
                            'DEP_DEL15': 'Departure delayed',
                            'ARR_DEL15': 'Arrival delayed',
                            'CANCELLED': 'Cancelled',
                            'DIVERTED': 'Diverted',
                            'DISTANCE': 'Distance',
                            'departure_delay': 'Departure delay'})
              )

    # Merge airports into flights
    flights = (pd.merge(flights, airports, left_on='Origin IATA', right_on='IATA')
                .drop(columns='IATA')
                .rename(columns={'Country': 'Origin country'})
                .merge(airports, left_on='Destination IATA', right_on='IATA')
                .drop(columns='IATA')
                .rename(columns={'Country': 'Destination country'})
         )

    # Import WHO data
    who = load_who_data('2020-02-01', '2020-03-01')

    return flights, who
