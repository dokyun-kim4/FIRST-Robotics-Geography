# FIRST-Robotics-Geography
Softdes 2023 Midterm Project  

Authors:  
Dexter Friis-Hecht & Dokyun Kim

# Project description
FIRST Robotics is an international robotics organization that has inspired thousands of teenagers, including us, to pursue STEM, with the majority of teams concentrated
in the United States. With the growth of the organization over time, there is value in not just geographically visualzing the teams for different years, but
also finding the factors that drive the growth of the organization. 

With FRC having a measured impact on the number of students entering STEM, knowing how and why the organization has spread poses the opportunity to find out how such spread can be applied to other educational organizations.

We first started with FIRST... that is, we gathered team location data from the FIRST API. With access to this, as well as some graphing packages such as Folium and Geopy, we can create a variety of visuals to answer our question:  
**What affects FRC team density across the US?**


# Required libraries
Before running any code, please install the following libraries:

`folium`  
`geopy`  
`pandas`  
`pytest`  
`requests`  

using `$pip install -r requirements.txt`

# Getting your own API key
Since you will be requesting data from the FIRST Robotics API, you need to get your own API-key.
## Steps:
1. Go to [The FIRST API website](https://frc-events.firstinspires.org/services/API) and click **Register for API Access**  

2. After registering, your username and authorization token will be sent in an email. 

3. Create a file named `apitoken.py` in both **DataFromFRC** and **Visualization** folders, and add the following line:  
`TOKEN = (<your username>, <your authorization token>)`

# Scraping FIRST data
The functions necessary for this step are in **DataFromFRC/**   

With helper functions in `frc_avatar_functions.py` and `frc_data_functions.py`, you can obtain various information about FRC teams such as:  
- Team number
- Team name
- Team location
- Team avatar
- And more

## Example code:  
`extract_data_all_pages(year=2020,make_csv=True)` will create a .csv file named **FRC2020.csv** in the root directory. Using **make_csv=False** will return a dataframe object instead of creating a .csv file. 

`decode_png_one_year(year=2020)` will add .png files of every team's avatar from the year 2020 in the **Avatars/2020/** directory as **\<teamnumber\>.png**

# Visualization
The functions necessary for this step are in **Visualization/**    
## Getting coordinates for teams
With helper functions in `get_geo_data.py`, you can take a team's location and get its coordinates to plot on a map.


### Example code:
`geo_data(year=2020,start=0,end=500)` will take the first 500 entries from **FRC2020.csv** and query their location through the geopy library. It then saves the latitude and longitude of each team in **Location/2020/** as **0-500.csv** that also contains:
- Team number
- Team name
- Location

Due to geopy's query limit, we suggest querying 500 at a time, but this number could decrease/increase depending on your internet connection.

After creating all the .csv files, run `merge_csv(2020)` to combine all the files into **2020Location.csv**

## Creating the map
With helper functions in `generate_usa_map`, you can:
- Create an empty US map - `usa_map_initialize()`
- Create a US map with avatars as markers for every team - `usa_map_with_avatar(year: int)`
- Create a Marker cluster map - `markercluster_map(year: int)`
- Create a Heatmap - `heat_map(year: int)`
- Overlay sponsor locations on a map - `add_sponsor(us_map: folium.Map)`

## Creating graphs
With helper functions in `pop_team_density_comparison.py`, you can plot FRC data against the US 2020 census.  
(contained in **Location/PopulationDensity/StatePopulationDensity.csv**)

### Example code:
`plot_frc_team_count(year=2020)` creates a bar graph showing how many FRC teams each state had in 2020

`graph_all_team_counts()` creates a bar graph showing how many FRC teams were in the US from 2015 to 2022

`plot_density_comparison(2020)` creates a bar graph showing FRC teams per 100,000 people per state from 2020
