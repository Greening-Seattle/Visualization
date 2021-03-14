# Visualization (Team Members: Sarah Pristash, Wenqi Cui and Shaun Gallagher)

The goal of this project is traffic visualization for the city of Seattle. There is a large quantity of publicly available data, including information about Average Annual Daily Traffic (AADT) and a specific GeoBaseID which expresses the location of these traffic counts in geospatial coordinates. These data are provided by the city and state governments on a yearly basis. This dataset can be used to better understand trends in traffic flow. In particular, the Greening Seattle Team wants to vizualize traffic trends at different levels of granularity, on both the Street and Census Track level. Data has been collected and cleaned in the Greening Seattle Shared Repository. This repository takes these data, in geoPandas data frames and visualizes them using Follium. The visualization of Seattle Traffic Data is intended to ultimately examine the impact of population growth on yearly traffic, and examine how urban planning strategies like construction of bike lanes, parking spaces or bike racks affect traffic flow in a specific area.   

- The public datasets from the city of Seattle that are being visualized include Bike Lanes, Bike Racks, population and traffic flow. All of these data have been aggregated by census tract. 
- The primary intended users are Seattle Residents or local officials who want to understand the impact of past and future Light Rail Expansion on traffic flow.


## Visualization Use Cases:

This project is intended to provide visual insight into Seattle's traffic patterns by examining key regions and exploring traffic changes over time. This project also includes generalizable methods for visualizing the traffic paterns of other cities beyond Seattle. As such these outputs can be useful to a wide audience. There are two key Use Cases for this project.  

### 1. Traffic visualization for informed urban planning:   
- User: Citizens, policy makers, environmental groups; 

- Function: To Map historical data in an interactive visual manner

- Key Result: A interactive map of Seattle that allows the user to look at Trafic flow patterns for cenus tracts within the city of Seattle over different years. This interactive map allows the user to view Chlorpleth Maps, which show traffic volume in geographic regions. Other key figure outputs are included within the repository as HTML files as well as being included below as "Screenshots."   

### 2. Expressing future predictions for Seattle Traffic flow:
Visualize Machine Learning Model Outputs from the Greening Seattle Prediction Team. 

- User: Citizens, policy makers, environmental groups; provide region of interest
- Function: Map predicted traffic/emissions reductions based on our predictive model
- Results:A  Map of predictions that can be varied with time


## Key files within the Repository:

- Chloropleth Map: A map of Seattle traffic flow for 2015 which has a color scale for traffic volume plotted against different census tracks.

- Map Building: A jupyter example notebook that contains instructions on building a chlorpleth map. 

- Documentation Folder: Contains use cases and component specification files.
 

 ## Key files within the Repository:
 





## Screenshots:

## License:
An open source MIT License for the project repository.


