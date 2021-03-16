## Component specs:

- On the development end, we will need to input traffic data and geospatial data. This can be accomplished with the GeoPandas package, which is a package designed to manage geo dataframes, similar to dataframes in pandas. One advantage of the GeoPandas package is that it contains the Shapely module, which enables the merging of data by geographic feature.  

- The user will access the data using GeoPandas, this has been specifically coded for the city of Seattle data in the get_geodata.py. The user can specify a year and this function will provide them with a cleaned GeoDataFrame. 

- The map function pyplot interfaces with databases of historical datasets from the city of Seattle to be able to represent data over time. This can be visualized in the project Python environment by making a Chloropleth plot. 

- The map will also interface with the prediction model to be able to display predicted changes in traffic flow. The output of this module is percent change in traffic flow.
