import fiona.crs
import folium
import geopandas as gpd
import geojson
import matplotlib.pyplot as plt
import numpy as np
import requests
import urllib.request as request

def plot_zip_traffic_data(year):
    '''function that takes a user input for a year and plots Seattle traffic data by zipcode.'''

    url_list = ['https://opendata.arcgis.com/datasets/7015d5d46a284f94ac05c2ea4358bcd7_0.geojson',
            'https://opendata.arcgis.com/datasets/5fc63b2a48474100b560a7d98b5097d7_1.geojson',
            'https://opendata.arcgis.com/datasets/27af9a2485c5442bb061fa7e881d7022_2.geojson',
            'https://opendata.arcgis.com/datasets/4f62515558174f53979b3be0335004d3_3.geojson',
            'https://opendata.arcgis.com/datasets/29f801d03c9b4b608bca6a8e497278c3_4.geojson',
            'https://opendata.arcgis.com/datasets/a0019dd0d6464747a88921f5e103d509_5.geojson',
            'https://opendata.arcgis.com/datasets/40bcfbc4054549ebba8b5777bbdd40ff_6.geojson',
            'https://opendata.arcgis.com/datasets/16cedd233d914118a275c6510115d466_7.geojson',
            'https://opendata.arcgis.com/datasets/902fd604ecf54adf8579894508cacc68_8.geojson',
            'https://opendata.arcgis.com/datasets/170b764c52f34c9497720c0463f3b58b_9.geojson',
            'https://opendata.arcgis.com/datasets/2c37babc94d64bbb938a9b520bc5538c_10.geojson',
            'https://opendata.arcgis.com/datasets/a35aa9249110472ba2c69cc574eff984_11.geojson']
    

    def get_gdf(year):
        '''Enter the desired year to download the traffic flow count
        data for that year. Example: enter '7' for the year 2007.
        '''

        num = year-7
        gdf_year = gpd.read_file(url_list[num])
        if year == 11:
            gdf_year = gdf_year.rename(columns={"YEAR_" : 'YEAR'})
            gdf_year = gdf_year[gdf_year.STNAME != '16TH AVE S']
        if year == 12:
            gdf_year = gdf_year.rename(columns={'STDY_YEAR' : 'YEAR'})
        if year == 15 or year == 16:
            gdf_year = gdf_year.rename(columns={"COUNTAAWDT" : 'AAWDT', "FLOWSEGID" : "GEOBASID", 'FIRST_STNAME_ORD' : 'STNAME'})
            gdf_year = gdf_year[['AAWDT', 'GEOBASID', 'STNAME', 'SHAPE_Length', 'geometry']]
            if year == 15:
                year_list = [2015]*len(gdf_year)
                gdf_year['YEAR'] = year_list
            elif year == 16:
                year_list = [2016]*len(gdf_year)
                gdf_year['YEAR'] = year_list
        elif year == 17 or year == 18:
            gdf_year = gdf_year.rename(columns={"AWDT" : 'AAWDT', "FLOWSEGID" : "GEOBASID", 'STNAME_ORD' : 'STNAME'})
            gdf_year = gdf_year[['AAWDT', 'GEOBASID', 'STNAME', 'SHAPE_Length', 'geometry']]
            if year == 17:
                year_list = [2017]*len(gdf_year)
                gdf_year['YEAR'] = year_list
            elif year == 18:
                year_list = [2018]*len(gdf_year)
                gdf_year['YEAR'] = year_list
        gdf_year = gdf_year[[ 'YEAR', 'AAWDT', 'GEOBASID', 'STNAME', 'SHAPE_Length', 'geometry']]
        gdf_year = gdf_year[gdf_year.YEAR != 0]
        gdf_year = gdf_year[gdf_year.YEAR.notnull()]
        return gdf_year 

    def get_census_bounds():
        url = 'https://opendata.arcgis.com/datasets/de58dc3e1efc49b782ab357e044ea20c_9.geojson'
        census_bounds = gpd.read_file(url)
        census_columns = ['NAME10', 'SHAPE_Area', 'geometry']
        census_bounds_cleaned = census_bounds.loc[:,census_columns]
        census_bounds_cleaned['NAME10'] = census_bounds_cleaned['NAME10'].astype(float)
        return census_bounds_cleaned


    def get_zipcode_bounds():
        zipcodes_url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
        zipcodes = gpd.read_file(zipcodes_url)

        zipcodes_columns = ['ZIPCODE', 'SHAPE_Area', 'geometry']
        zipcodes_cleaned = zipcodes.loc[:,zipcodes_columns]
        zipcodes_cleaned['ZIPCODE'] = zipcodes_cleaned['ZIPCODE'].astype(int)
        zipcodes_cleaned.head()

        census_bounds_cleaned = get_census_bounds()
        zips = gpd.sjoin(zipcodes_cleaned, census_bounds_cleaned, op='intersects')
        zips_columns = ['ZIPCODE', 'NAME10', 'SHAPE_Area_left', 'geometry']
        zips = zips[zips_columns]

        zips = zips.dissolve(by='ZIPCODE')
        return zips
    
    zips = get_zipcode_bounds()
    gdf_year = get_gdf(year)
    
    city_by_zip = gpd.sjoin(zips, gdf_year, op='intersects')
    traffic_zones = city_by_zip.dissolve(by='ZIPCODE', aggfunc = 'sum')
    traffic_zones.reset_index(inplace = True)
    traffic_zones = traffic_zones[['GEOBASID', 'AAWDT', 'ZIPCODE', 'geometry']]
    traffic_zones_json = traffic_zones.to_json()
    
    # Create a Map instance
    m = folium.Map(location=[47.65, -122.3], tiles = 'cartodbpositron', zoom_start=10, control_scale=True)

    # Plot a choropleth map
    # Notice: 'geoid' column that we created earlier needs to be assigned always as the first column
    folium.Choropleth(
        geo_data=traffic_zones_json,
        name='Average Annual Weekly Daily Traffic Flow 2015',
        data=traffic_zones,
        columns=['GEOBASID', 'AAWDT'],
        key_on='feature.properties.GEOBASID',
        fill_color='RdYlBu_r',
        fill_opacity=0.7,
        line_opacity=0.2,
        line_color='white', 
        line_weight=2,
        highlight=False, 
        smooth_factor=1.0,
        #threshold_scale=[100, 250, 500, 1000, 2000],
        legend_name= 'Traffic Counts').add_to(m)

    # Convert points to GeoJson
    folium.features.GeoJson(traffic_zones,  
                            name='Labels',
                            style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
                            tooltip=folium.features.GeoJsonTooltip(fields=['ZIPCODE','AAWDT'],
                                                                    aliases = ['Zipcode','Traffic Count'],
                                                                    labels=True,
                                                                    sticky=False
                                                                                )
                           ).add_to(m)

    #Show map
    m
    
    return m
    
    
        
