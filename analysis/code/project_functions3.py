def load_airline_information(url_path = '../data/raw/Jan_2020_ontime.csv'):
    #Method chain 1: load and clean data the raw data
    
    df1 = ((pd.DataFrame(data=pd.read_csv('../data/raw/Jan_2020_ontime.csv')))
           .drop(columns=['OP_UNIQUE_CARRIER', 'OP_CARRIER_AIRLINE_ID', 'TAIL_NUM', 'OP_CARRIER_FL_NUM', 'ORIGIN_AIRPORT_ID', 
                          'ORIGIN_AIRPORT_SEQ_ID', 'DEST_AIRPORT_ID', 'DEST_AIRPORT_SEQ_ID', 'DEP_TIME_BLK', 'Unnamed: 21'])
           .dropna(subset=['DEP_TIME', 'DEP_DEL15', 'ARR_TIME', 'ARR_DEL15'])
          )

    
    #Method chain 2: clean and substitute values in the cleaned raw data to 
    df2 = (df1       
              .rename(columns={'DAY_OF_MONTH':'Day of Month', 'DAY_OF_WEEK':'Day of Week', 'OP_CARRIER':'Airline_Code', 
                               'DEP_TIME':'Departure_Time', 'DEP_DEL15':'Delayed_Departure', 'ARR_TIME':'Arrival_Time', 'ARR_DEL15':'Delayed_Arrival',
                              'CANCELLED':'Is_Cancelled', 'DIVERTED':'Is_Diverted', 'DISTANCE':'Miles_Flown'})
              .assign(Delayed_Departure = lambda x: np.where(x['Delayed_Departure'] == 0, False,True))
              .assign(Delayed_Arrival = lambda x: np.where(x['Delayed_Arrival'] == 0, False,True))
              .assign(Is_Cancelled = lambda x: np.where(x['Is_Cancelled'] == 0, False,True))
              .assign(Is_Diverted = lambda x: np.where(x['Is_Diverted'] == 0, False,True))
          )
    
    df3 = (df2
              .replace({'Airline_Code':'EV'}, 'ExpressJet')
              .replace({'Airline_Code':'WN'}, 'Southwest Airlines')
              .replace({'Airline_Code':'MQ'}, 'Envoy Air')
              .replace({'Airline_Code':'B6'}, 'JetBlue')
              .replace({'Airline_Code':'HA'}, 'Hawaiian Airlines') 
              .replace({'Airline_Code':'AA'}, 'American Airlines') 
              .replace({'Airline_Code':'F9'}, 'Frontier Airlines')        
              .replace({'Airline_Code':'YX'}, 'Republic Airways')
              .replace({'Airline_Code':'9E'}, 'Endeavor Air')
              .replace({'Airline_Code':'YV'}, 'Mesa Airlines')
              .replace({'Airline_Code':'OH'}, 'PSA Airlines')
              .replace({'Airline_Code':'NK'}, 'Spirit Airlines') 
              .replace({'Airline_Code':'DL'}, 'Delta Airlines')
              .replace({'Airline_Code':'OO'}, 'SkyWest Airlines') 
              .replace({'Airline_Code':'UA'}, 'United Airlines') 
              .replace({'Airline_Code':'G4'}, 'Allegiant Air')
              .replace({'Airline_Code':'AS'}, 'Alaska Airlines')
              .rename(columns={'Airline_Code':'Airline'})       
              #this airline_df will display the delays, cancellations, and diverts of each airline so here I drop the irrelevant columns for this certain data frame
              .drop(columns=['Day of Week', 'ORIGIN', 'DEST','Departure_Time', 'Arrival_Time'])     
          )
    return df3
