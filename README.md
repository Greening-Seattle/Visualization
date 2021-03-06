[![Build Status](https://www.travis-ci.com/Greening-Seattle/Visualization.svg?branch=main)](https://www.travis-ci.com/Greening-Seattle/Visualization)

# Green Seattle-Visualization<br /> (Team Members: Sarah Pristash, Wenqi Cui and Shaun Gallagher)

The goal of this project is traffic visualization for the city of Seattle. There is a large quantity of publicly available data, including information about Average Annual Daily Traffic (AADT) and a specific GeoBaseID which expresses the location of these traffic counts in geospatial coordinates. These data are provided by the city and state governments on a yearly basis. This dataset can be used to better understand trends in traffic flow. In particular, the Greening Seattle Team wants to vizualize traffic trends at different levels of granularity, on both the Street and Census Track level. Data has been collected and cleaned in the Greening Seattle Shared Repository. This repository takes these data, in geoPandas data frames and visualizes them using Follium. The visualization of Seattle Traffic Data is intended to ultimately examine the impact of population growth on yearly traffic, and examine how urban planning strategies like construction of bike lanes, parking spaces or bike racks affect traffic flow in a specific area.   

- The public datasets from the city of Seattle that are being visualized include Bike Lanes, Bike Racks, population, population fraction and traffic flow. All of these data have been aggregated by zip code.

- Zip codes were chosen as the geographic level to examine because it exists as an intermediate level, minimizing the tradeoff between minimal features in smaller regions and inability to see broader trends in the data sets with  city-wide view. 
 
- The primary intended users are Seattle Residents or local officials who want to understand and predict the effects of population growth and local transit infrastructure on traffic flow.


## Visualization Use Cases:

This project is intended to provide visual insight into Seattle's traffic patterns by examining key regions and exploring traffic changes over time. This project also includes generalizable methods for visualizing the traffic paterns of other cities beyond Seattle. As such these outputs can be useful to a wide audience. There are two key Use Cases for this project.  

### 1. Traffic visualization for informed urban planning:
   
- User: Citizens, policy makers, environmental groups; 

- Function: To map historical data in an interactive visual manner. The key component here is 'plotting_functions.py' which can generate map data.

- Key Result: An interactive map of Seattle that allows the user to look at Trafic flow patterns on a per year basis by zipcode. This interactive map allows the user to view Chlorpleth Maps, which show traffic volume in geographic regions. Other key figure outputs are included within the repository as HTML files as well as being included below as "Screenshots."   

### 2. Expressing future predictions for Seattle Traffic flow:
Visualize Machine Learning Model Outputs from the Greening Seattle Prediction Team. 

- User: Citizens, policy makers, environmental groups; provide region of interest

- Function: Map predicted traffic/emissions reductions based on our predictive model

- Results: A Map of predictions that can be varied with time. This output was demonstrated for the in class presentation.

### 3. Framework for Visualizing the training of neural network for prediction:
Visualize the Traning Process of Machine Learning Model from Tensorboard 

- User: Policy makers or researchers who train an neural network for prediction

- Function: Train a neural network for predicting the traffic data based on the input features

- Results: Tensorboard for visualzing the training process, the neural network for prediction. After the prediction group trains the model and predicts traffic flow the visualization team will contextualize these model outputs.


### Visual Examples of Key Results:

Example of Demo Interactive Chloropleth Map:

![Demo Seattle Map](https://github.com/Greening-Seattle/Visualization/blob/main/map_html/demo_map.PNG)

-Example of breaking down geographic data by specific areas, here University District Census Tracts:

![University Census Tract](https://github.com/Greening-Seattle/Visualization/blob/main/map_html/U%20District%20Area%20Chloropleth%20Plot.PNG)

-Example of Visualizing Dense Neural Network Outputs: 

-This is an example of the Visualization Team taking the output of the machine learning model developed by the prediction team.

![ML Traffic Visualization](https://github.com/Greening-Seattle/Visualization/blob/main/map_html/Change%20in%20traffic%20with%202.5%20population%20change.PNG) 


## Key files within the Repository:

- Chloropleth Map: A map of Seattle traffic flow for 2015 which has a color scale for traffic volume plotted against different census tracks.

- Map Building: An example jupyter notebook that contains instructions on building a chlorpleth map. 

- Documentation Folder: Contains use cases and component specification files.

- The process for data cleaning can be viewed on the Shared Repository and Prediction Repository for the Greening Seattle Organization. 

- tests/ contains unit tests for key functions within the repository, as well as for continuous integtration with Travis.

- source/ contains sketch jupyter notebook that provide helpful examples for users in working with the Geographic data.

- visualization/ contains plotting function to express traffic data as an interactive Chlorpleth Map in follium

- map_html Several example versions of chloropleth maps

- Model Visualization/ Frameworks for training a neural network for prediction and visualizing the training process. It also include the module to exporting the tensorflow-formated model to the Numpy-formated model.   

## Repository Architecture:

```
|   README.md
|   LICENSE
|   .travis.yml
|   .gitignore
|   _config.yml
|   index.md 
+---Documentation
|   |   Use_Cases.md
|   |   Components.md
+---Model Visualization 
|   |   Predict_Visualize_Traffic_MultiFeature.ipynb
|   |   Predict_power_comsumption_v2.ipynb
|   |   volkswagen_e_golf.csv
|   |   all_data.csv
|   |
+---greening_vis 
|   +---tests
|   |   __init__.py
|   |   plotting_functions.py
+---map_html
|   |   U District Area Chloropleth Plot.PNG
|   |   choropleth_map.html
|   |   choropleth_mapv2.html
|   |   choropleth_mapv3.html
|   |   demo_map.PNG
+---source
|   |    Map building.ipynb
|   |    Mapping_function_test.ipynb
|   |    SG Tests_get gdf.ipynb
|   |    Change in traffic with 2.5 population change.PNG
```

## Code References
We thank the following references for providing open-source data

- City of Seattle Public Data https://data.seattle.gov/
- Electric Vehicle: https://github.com/armiro/crawlers/tree/master/SpritMonitor-Crawler

## License:
An open source MIT License for the project repository.


