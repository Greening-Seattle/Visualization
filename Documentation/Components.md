## Component specs:

- On the development end, we will need to input traffic data and geospatial data. This can be accomplished with the GeoPandas package, which is a package designed to manage geo dataframes, similar to dataframes in pandas. One advantage of the GeoPandas package is that it contains the Shapely module, which enables the merging of data by geographic feature.  

- The User will access the map and be able to vary the year to observe Seattle traffic flow over time.

- The map will need to interface with databases of historical datasets to be able to represent data over time. This can be visualized in the project Python environment by making a Chloropleth plot. 

- The map will also need to interface with the prediction model to be able to display predicted changes.
