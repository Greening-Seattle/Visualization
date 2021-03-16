import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import requests
url_list = [
 'https://opendata.arcgis.com/datasets/7015d5d46a284f94ac05c2ea4358bcd7_0.geojson',
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
    
    # Pulls the data from Seattle's open GIS.
    num = year-7
    gdf_year = gpd.read_file(url_list[num])
    # There are some inconsistencies in the names of columns across years in this data, 
    # so these conditional statements make everything the same.
    if year == 11:
        gdf_year = gdf_year.rename(columns={"YEAR_":'YEAR'})
        gdf_year = gdf_year[gdf_year.STNAME != '16TH AVE S']
    if year == 12:
        gdf_year = gdf_year.rename(columns={'STDY_YEAR':'YEAR'})
    if year == 15 or year == 16:
        gdf_year = gdf_year.rename(columns={"COUNTAAWDT":'AAWDT',\ 
        "FLOWSEGID":"GEOBASID", 'FIRST_STNAME_ORD':'STNAME'})
        gdf_year = gdf_year[['AAWDT', 'GEOBASID', 'STNAME',\
        'SHAPE_Length', 'geometry']]
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
    # This cleans the output to contain only relevant columns.
    gdf_year = gdf_year[[ 'YEAR', 'AAWDT', 'GEOBASID', 'STNAME', 'SHAPE_Length', 'geometry']]
    # This removes any null values from the dataset. 
    gdf_year = gdf_year[gdf_year.YEAR != 0]
    gdf_year = gdf_year[gdf_year.YEAR.notnull()]
    return gdf_year 

def get_census_bounds():
    ''' Downloads boundaries of census tracts for the city of Seattle. Data comes from Seattle's open GIS data.'''
    # First, we download the data from Seattle's open GIS. 
    url = 'https://opendata.arcgis.com/datasets/de58dc3e1efc49b782ab357e044ea20c_9.geojson'
    census_bounds = gpd.read_file(url)
    # We select only the relevant columns.
    census_columns = ['NAME10', 'SHAPE_Area', 'geometry']
    census_bounds_cleaned = census_bounds.loc[:,census_columns]
    # We change the cenus tract name to an integer for manipulation later.
    census_bounds_cleaned['NAME10'] = census_bounds_cleaned['NAME10'].astype(float)
    return census_bounds_cleaned


def get_zipcode_bounds():
    ''' Downloads boundaries of zipcodes for the city of Seattle. Data comes from Seattle's open GIS data.'''
    # First, we download the data from Seattle's open GIS.
    zipcodes_url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    zipcodes = gpd.read_file(zipcodes_url)
    # We select only the relevant columns and change the Zipcode to an integer for manipulation later.
    zipcodes_columns = ['ZIPCODE', 'SHAPE_Area', 'geometry']
    zipcodes_cleaned = zipcodes.loc[:,zipcodes_columns]
    zipcodes_cleaned['ZIPCODE'] = zipcodes_cleaned['ZIPCODE'].astype(int)
    zipcodes_cleaned.head()
    # The zipcode dataset includes more than just the area of Seattle, so we join it 
    # with the census bounds to get out only Seattle data. 
    census_bounds_cleaned = get_census_bounds()
    zips = gpd.sjoin(zipcodes_cleaned, census_bounds_cleaned, op='intersects')
    zips_columns = ['ZIPCODE', 'NAME10', 'SHAPE_Area_left', 'geometry']
    zips = zips[zips_columns]
    # Finally, we dissolve the data by Zipcode to ensure one area for each zipcode.
    zips = zips.dissolve(by='ZIPCODE')
    return zips

def plot_zip_traffic_data(year):
    '''function that takes a user input for a year and plots Seattle traffic data by zipcode.'''
    
    # We need to download the zipcode data and the traffic data for the desired year. 
    zips = get_zipcode_bounds()
    gdf_year = get_gdf(year)
    
    # A spatial join of the traffic data with the zipcodes assigns each street to its respective
    # zip code. Then, we dissolve this data set by zipcode so that each zipcode is one row with 
    # the cumulative traffic count associated with it. We also convert the data to a json for the 
    # map feature.
    city_by_zip = gpd.sjoin(zips, gdf_year, op='intersects')
    traffic_zones = city_by_zip.dissolve(by='ZIPCODE', aggfunc = 'sum')
    traffic_zones.reset_index(inplace = True)
    traffic_zones = traffic_zones[['GEOBASID', 'AAWDT', 'ZIPCODE', 'geometry']]
    traffic_zones_json = traffic_zones.to_json()
    
    # Folium tutorial that informed this code:
    # https://autogis-site.readthedocs.io/en/latest/notebooks/L5/02_interactive-map-folium.html
    # Stackoverflow question that helped create the tooltips: 
    # https://stackoverflow.com/questions/55088688/how-do-you-add-geojsontooltip-to-folium-choropleth-class-in-folium
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

def get_agg_year():
    year_list = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    agg_year_data = gpd.GeoDataFrame()
    for year in year_list:
        agg_year_data = agg_year_data.append(get_gdf(year))  
    return agg_year_data

def plot_traffic_data_over_time():
    '''Function that plots all Seattle traffic data by zipcode over the time period 2007-2018.'''
    
    print('Function takes a moment to run. Please wait.')
    
    # Aggregate all traffic data by year
    agg_year_data = get_agg_year()
    
    # Download zip bounds
    zip_bounds = get_zipcode_bounds()
    # Set aggregated year data to zip bound coordinate system
    agg_year_data.crs = zip_bounds.crs
    # Spatial join the aggregated traffic data with the zip codes to get zipcode for each street points
    city_by_zip = gpd.sjoin(zip_bounds, agg_year_data, op='intersects')
    city_by_zip.reset_index(inplace = True)
    # Select only the necessary columns
    city_by_zip = city_by_zip[['GEOBASID','ZIPCODE', 'YEAR', 'AAWDT', 'geometry']]
    # Dissolve data by zipcode and year to aggregate data within geographic area
    # and keep year info.
    zips_years = city_by_zip.dissolve(by=['YEAR','ZIPCODE'], aggfunc=sum)
    zips_years.reset_index(inplace=True)
    
    # TimeSliderChoropleth example found here:
    # https://www.analyticsvidhya.com/blog/2020/06/guide-geospatial-analysis-folium-python/
    from folium.plugins import TimeSliderChoropleth
    # Convert time data from just year to year-month-day format
    zips_years['ModifiedDateTime'] = pd.Series(pd.to_numeric(zips_years['YEAR'], errors='coerce'), dtype='int64')
    zips_years.ModifiedDateTime.fillna(0)
    zips_years['ModifiedDateTime'] = zips_years['ModifiedDateTime']*1e4+101
    zips_years['ModifiedDateTime'] = pd.to_datetime(zips_years['ModifiedDateTime'].astype('int64').astype('str'))
    # Convert traffic data from strings to numbers
    zips_years['AAWDT'] = zips_years['AAWDT'].astype(int)
    # Create bins for choropleth scale
    bins=np.linspace(min(zips_years['AAWDT']),max(zips_years['AAWDT']),11)
    # Create color column for AAWDT data based on RdYlBu_r hex keys
    zips_years['color'] = zips_years['AAWDT']=pd.cut(zips_years['AAWDT'],bins,labels=['#313695',\
        '4575b4','#74add1','#abd9e9','#e0f3f8','#ffffbf','#fee090',\
        '#fdae61','#f46d43','a50026'],include_lowest=True)
    # Select relevant columns
    zips_years = zips_years[['ModifiedDateTime', 'ZIPCODE', 'AAWDT', 'color', 'geometry']]
    # Convert time to ms format needed for TimeSliderChoropleth
    zips_years['ModifiedDateTime']=(zips_years['ModifiedDateTime'].astype(int)// 10**9).astype('U10')
    # Make zipcodes a str for the map
    zips_years['ZIPCODE'] = zips_years['ZIPCODE'].astype(str)
    # Create a style dictionary for the map
    traffic_dict={}
    for i in zips_years['ZIPCODE'].unique():
        traffic_dict[i]={}
        for j in zips_years[zips_years['ZIPCODE']==i].set_index(['ZIPCODE']).values:   
            traffic_dict[i][j[0]]={'color':j[1],'opacity':0.8}
    
    m2 = folium.Map([47.65, -122.3], tiles='cartodbpositron', zoom_start=10)

    g = TimeSliderChoropleth(
        zips_years.set_index('ZIPCODE').to_json(),
        styledict=traffic_dict
    ).add_to(m2)

    return m2
    
    
    
    
        


    
