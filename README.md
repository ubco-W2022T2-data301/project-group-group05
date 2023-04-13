# Group 05 - Frustrated Flyers

![A poorly drawn logo](./images/logo.svg)

Analyzing COVID-19's impact on commercial airlines and their passengers.

## Presentation

Our dashboard presentation is available in the video below.

[![DATA 301 Dashboard Presentation](https://i.ytimg.com/vi/_aQ1W5y54HM/maxresdefault.jpg)](https://www.youtube.com/watch?v=_aQ1W5y54HM "DATA 301 Dashboard Presentation")

## Milestones

- [x] Milestone 1
	- [x] Add data
	- [x] Add project vision
- [x] Milestone 2
	- [x] Add analyses
	- [x] Fill out README
- [x] Milestone 3
	- [x] Complete EDAs
	- [x] Revise research questions
- [x] Milestone 4
    - [x] Partial analysis pipelines
        - [x] Step-by-step pipeine
        - [x] Rewrite with method chaining
    - [x] Create `project_functions.py` files
    - [x] Conduct analysis
- [x] Milestone 5
    - [x] Update the processed dataset for Tableau Dashboard if needed
    - [x] Create Tableau Dashboards
    - [x] Record a 10 minute video presenting the dashboard
- [x] Milestone 6
    - [x] Address project feedback
    - [x] Write final report

## Contract requirements
- [x] Implement project feedback
    - [x] Feedback 1
    - [x] Feedback 2
    - [x] Feedback 3
    - [ ] ~~Feedback 4~~
- [x] Data loading
- [x] Complex data visualization
- [x] Appropriate titles and labels for all plots
- [x] At least one key insight per plot
- [x] Complex data cleaning, wrangling, processing
    - [x] Handle missing values
    - [x] Update column names
    - [x] Remove unnecessary columns
    - [x] Use groupby objects
    - [x] Create aggregate dataframe
- [x] Complex research questions
- [x] Narrative with insightful commentary
- [x] Sophisticated Tableau Dashboard
- [x] Use of functions in wrangling, processing, cleaning
- [x] 4+ basic operations
- [x] 3+ advanced operations
- [x] 2+ method chains
- [x] Use of git branches
- [x] Use of GitHub features
    - [x] Pull requests
    - [x] Code reviews
    - [x] Issues
- [x] Extra flair (we hope)

## Describe your topic/interest in about 150-200 words

We are interested in how airlines initially responded to COVID-19, how those responses disrupted consumer flights, and how we can use flight and health data to predict flight delays and cancellations during future pandemics.

Despite their sound engineering and safety protocols, airlines are still at the mercy of nature. They contend with various logistical challenges that create turbulence in their operation such as the winter storm in December 2022 that left many UBCO students unable to see their families.

In the wake of this, we are investigating flight delays and cancellations during COVID-19 due to the wealth of data available during that period. By analyzing this data, relating them to specific airlines, and comparing the effects of COVID-19 in different regions, we hope to predict these disruptions.

We are also interested in relating the flight data to notable events in the early timeline of COVID-19, e.g., its first reported fatality, the health emergency declared in the United States, and the second case in Thailand. Spikes in flight delays might relate to such health events, so gaining insight into them might improve our predictions.

## Describe your dataset in about 150-200 words

Unlike weather issues, which have always been a factor in aviation, an international pandemic would have been an extraordinary circumstance for airlines. Therefore, we aim to understand how airlines handled the pandemic by analyzing their flights near the beginning of the pandemic. The first known case was in December 2019, so any data during or after that month should be relevant.

Our dataset contains a list of flights from January 2020 sourced from the US Government. For each flight, it lists the IATA codes for origin and destination airports, the distance of each flight, the tail number of the aircraft, the date of the flights, and other values. Most notably, it also contains both the planned and actual times of departure and arrival times, and it tells us whether the flight was diverted or canceled. This allows us to find information about flight delays without having to futz around with multiple data sources.

If possible, we will incorporate health data and airport location data in the near future.

## Team Members

- Bradan Fleming: I need a hug.
- Aakash Tirathdas: Need to fix my sleep schedule.
- Kaiden Merchant: I need a car :(

## Images

{You should use this area to add a screenshot of an interesting plot, or of your dashboard}

<img src ="images/test.png" width="100px">

## References

- [January Flight Delay Prediction](https://www.kaggle.com/datasets/divyansh22/flight-delay-prediction)
    - License: [U.S. Government Works](https://www.usa.gov/government-works/)
- [February Flight Delay Prediction](https://www.kaggle.com/datasets/divyansh22/february-flight-delay-prediction)
    - License: [U.S. Government Works](https://www.usa.gov/government-works/)
- [Daily cases and deaths by date reported to WHO](https://covid19.who.int/data)
    - License: [CC BY-NC-SA 3.0 IGO](https://creativecommons.org/licenses/by-nc-sa/3.0/igo/)
- [OpenFlights extended airport data](https://openflights.org/data.html)
    - License: [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)
