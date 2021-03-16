import fiona.crs
import folium
import geopandas as gpd
import geojson
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import urllib.request as request

import plotting_functions
from plotting_functions import plot_zip_traffic_data
from plotting_functions import plot_traffic_data_over_time
from plotting_functions import get_agg_year
from plotting_functions import get_gdf

def test_plot_zip_traffic_data(year):
    inputs = list(range(7,19))
    years = list(range(2007,2019))
    year_dict = dict(zip(inputs,years))
    
    gdf_year = get_gdf(year)
    year_test = gdf_year['YEAR'].unique().astype(int)[0]
    
    assert year_dict.get(year) == year_test, 'Function downloaded incorrect year data'
    return

def test_plot_traffic_data_over_time():
    agg_year_data = get_agg_year()
    year_expect = np.array(range(2007,2019))
    year_prod = agg_year_data['YEAR'].unique()
    assert np.array_equal(year_prod,year_expect), 'Aggregation of data by year did not occur correctly'
    return