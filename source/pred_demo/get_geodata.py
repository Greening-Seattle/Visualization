import pandas as pd    
import geopandas as gpd
import urllib.request as request


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

def get_seattle_dataset():
    
    def get_rack_data():
        # This data is downloaded from Seattle Open GIS
        racks_url = 'https://opendata.arcgis.com/datasets/f86c29ce743e47819e588c3d643ceb63_0.geojson'
        r = gpd.read_file(racks_url)
        # Selects wanted columns of dataframe, drops null values, and puts install date into terms of years to matcho other data
        racks = r[['INSTALL_DATE', 'RACK_CAPACITY', 'geometry']]
        racks = racks[racks.INSTALL_DATE.notnull()]
        racks['Year'] = pd.DatetimeIndex(racks['INSTALL_DATE']).year
        racks = racks.drop(columns='INSTALL_DATE')
        #filters rack data to the range 2007 - 2018, which is what we have traffic data for
        #also does a spatial join to put each rack with its associated zipcode
        racks_half_filtered = racks[racks['Year'] >= 2007]
        racks_filtered = racks_half_filtered[racks_half_filtered['Year'] <= 2018]
        racks_zips = gpd.sjoin(zips_sea, racks_filtered, op='contains')
        racks_zips.reset_index(inplace=True)
        #Dissolves data into single zipcode regions and sums through that region, then selects necessary columns for model 
        zips_racks = racks_zips.dissolve(by=["Year", "ZIPCODE"], aggfunc=sum)
        zips_racks.reset_index(inplace=True)
        zips_racks_clean = zips_racks[['Year', 'ZIPCODE', 'RACK_CAPACITY']]
        
        return zips_racks_clean

    def get_lane_data():
        # This data is downloaded from Seattle Open GIS
        bike_lanes_url = 'https://gisdata.seattle.gov/server/rest/services/SDOT/SDOT_Bikes/MapServer/1/query?where=1%3D1&outFields=OBJECTID,STREET_NAME,LENGTH_MILES,SHAPE,DATE_COMPLETED,SHAPE_Length&outSR=4326&f=json'
        bike_lanes = gpd.read_file(bike_lanes_url)
        # Initial selection of relevant columns
        lane_columns = ['LENGTH_MILES', 'DATE_COMPLETED', 'geometry']
        bike_lane = bike_lanes[lane_columns]
        #Converts the date completed column to year
        bike_lane['DATE_COMPLETED'] = pd.to_datetime(bike_lane['DATE_COMPLETED'], unit='ms')
        bike_lane['Year'] = pd.DatetimeIndex(bike_lane['DATE_COMPLETED']).year
        bike_lane = bike_lane.drop(columns='DATE_COMPLETED')
        # builds a baseline of bike lanes before 2007 to add cumulatively to the 2007-2018 data
        bike_lane['Year'] = bike_lane['Year'].fillna(0)
        bike_lane_baseline = bike_lane[bike_lane['Year'] <2007]
        zips_lane_base = gpd.sjoin(zips_sea, bike_lane_baseline, op='intersects')
        zips_lane_base.reset_index(inplace=True)
        zips_lane_base_diss = zips_lane_base.dissolve(by=['Year', 'ZIPCODE'], aggfunc = 'sum')
        zips_lane_base_diss.reset_index(inplace=True)
        zip_list = list(zips_lane_base_diss['ZIPCODE'].unique())
        year_fill = [0] *len(zip_list)
        zip_sum_list = []*len(zip_list)
        for zipcode in zip_list:
            selection = zips_lane_base_diss.loc[zips_lane_base_diss['ZIPCODE'] == zipcode]
            zip_sum = selection['LENGTH_MILES'].sum()
            zip_sum_list.append(zip_sum)
        base_df = pd.DataFrame(list(zip(zip_list, year_fill, zip_sum_list)), index = range(len(zip_list)), columns = ['ZIPCODE', 'Year', 'Miles_Bike_Lanes'] )
        #Filters bike lane data into years from 2007-2018, which is what we have traffic data for.
        bike_half_filtered = bike_lane[bike_lane['Year'] >= 2007]
        bike_filtered = bike_half_filtered[bike_half_filtered['Year'] <= 2018]
        #Does spatial join to put bikelanes with respective zipcode
        zips_bikelane = gpd.sjoin(zips_sea, bike_filtered, op='intersects')
        zips_bikelane.reset_index(inplace=True)
        #Dissolve into single zip code areas and aggregate the data within those areas
        zips_lanes = zips_bikelane.dissolve(by=['Year', 'ZIPCODE'], aggfunc=sum)
        zips_lanes.reset_index(inplace=True)
        #Selects relevant columns of data and renames quant variable for clarity
        zips_lanes_clean = zips_lanes[['Year', 'ZIPCODE', "LENGTH_MILES"]]
        zips_lanes_clean = zips_lanes_clean.rename(columns = {'LENGTH_MILES' : 'Miles_Bike_Lanes'})
        zips_lanes_clean = base_df.append(zips_lanes_clean)
        ## MATTS FUNCTION GOES HERE ##

        return zips_lanes_clean

    def get_sidewalk_data():
        
        return zip_sidewalk_clean

    def get_pop_data():
        #This data is downloaded from Seattle Open GIS
        pop_url_2010 = 'https://gisrevprxy.seattle.gov/arcgis/rest/services/CENSUS_EXT/CENSUS_2010_BASICS/MapServer/15/query?where=1%3D1&outFields=SHAPE,GEOID10,NAME10,ACRES_TOTAL,Total_Population,OBJECTID&outSR=4326&f=json'
        pop_2010 = gpd.read_file(pop_url_2010)
        # Redefines census tract geometries by their centroid points to avoid double counting when spatial join happens
        census_bounds_cleaned = get_census_bounds()
        census_cent = census_bounds_cleaned.copy()
        census_cent['geometry'] = census_cent['geometry'].centroid
        pop_2010['geometry'] = census_cent['geometry']
        # Spatial join to put populations with associated zipcode
        pop_zips = gpd.sjoin(zips_sea, pop_2010, op='contains')
        pop_zips.reset_index(inplace=True)
        pop_zips = pop_zips[['ZIPCODE','geometry', 'Total_Population']]
        # Dissolve into single zipcode geometry and aggregate within that geometry
        pop_zips_diss = pop_zips.dissolve(by='ZIPCODE', aggfunc='sum')
        pop_zips_diss.reset_index(inplace=True)
        pop_zips_diss_clean = pop_zips_diss[['ZIPCODE', 'Total_Population']]
        #Create estimates for zip code populations in years besides 2010 based on the population fraction and total population
        total_pop = pop_zips_diss_clean['Total_Population'].sum()
        pop_zips_diss_clean['Pop_fraction'] = pop_zips_diss_clean['Total_Population']/total_pop
        years = list(range(2007, 2019))
        populations = [585436, 591870, 598539, 608660, 622694, 635928, 653588, 670109, 687386, 709631, 728661, 742235]
        pop_by_year = dict(zip(years, populations))
        def est_zip_pop(year, pop_zips_diss_clean, pop_by_year):
            pop_frac = pop_zips_diss_clean['Pop_fraction'].values
            year_pop = pop_by_year.get(year)
            pop_zip_year = pop_zips_diss_clean.copy()
            pop_zip_year['Total_Population'] = pop_frac*year_pop
            return pop_zip_year
        
        pop_zips_years = gpd.GeoDataFrame()
        for year in years:
            pop_zip_year = est_zip_pop(year, pop_zips_diss_clean, pop_by_year)
            pop_zip_year['Year'] = year
            pop_zips_years = pop_zips_years.append(pop_zip_year)
        pop_zips_years = pop_zips_years[['Year', 'ZIPCODE', 'Total_Population', 'Pop_fraction']]
        return pop_zips_years
    
    def traffic(year):
        '''Function to generate distributions of traffic flow by year in each zip
        '''
        gdf_test = get_gdf(year)

        midpoints = gdf_test.copy()
        midpoints['MIDPOINT'] = gdf_test['geometry'].interpolate(0.5, normalized = True)
        midpoint_columns = ['YEAR', 'AAWDT', 'MIDPOINT']
        midpoint_cleaned = midpoints.loc[:,midpoint_columns]
        midpoint_cleaned['geometry'] = midpoint_cleaned['MIDPOINT']
    
        zip_mids = gpd.sjoin(zips,midpoint_cleaned,op='contains')
        zip_mids_clean = zip_mids.copy()
        zip_mids_clean = zip_mids_clean.drop(columns=['SHAPE_Area_left','NAME10','index_right','MIDPOINT'])
    
        zip_mids_clean_c = zip_mids_clean.copy()
        zip_mids_clean_c.drop_duplicates(inplace=True)
        zip_mids_clean_cc = zip_mids_clean_c.copy()
        zip_mids_clean_cc.drop(columns=['geometry'])
        zip_mids_clean_cc = zip_mids_clean_cc.dissolve(by=['ZIPCODE'],aggfunc=sum)
    
        zip_traffic = zip_mids_clean_cc.copy()
        zip_traffic.drop(columns=['geometry'],inplace=True)
        zip_traffic['YEAR'] = year + 2000
        zip_traffic.reset_index(inplace=True)
        zip_traffic = zip_traffic[['ZIPCODE', 'YEAR', 'AAWDT']]
        zip_traffic.head(n=30)

        return zip_traffic

    def total_traffic(years):
        df_total_traffic = pd.DataFrame()
        years = list(np.arange(7,19))
        for year in years:
            traffic_year = traffic(year)
            df_total_traffic = df_total_traffic.append(traffic_year)
        return df_total_traffic

    def final_df():
        '''Ultimate function that returns total compiled traffic data frame by year and zip
        '''
        years = list(np.arange(7,19))
        total_df = total_traffic(years)
        total_traffic_df = total_df.copy()
        total_traffic_df.groupby(by='ZIPCODE')
        total_traffic_df.sort_values(['ZIPCODE','YEAR'],inplace=True)

        return total_traffic_df

    rack_data = get_rack_data()
    lane_data = get_lane_data()
    sidewalk_data = get_sidewalk_data()
    pop_data = get_pop_data()
    traffic_data = final_df()

    a = pd.merge(traffic_data, pop_data, how='left', on= ['Year', 'ZIPCODE'])
    b = pd.merge(a, rack_data, how='left', on =['Year', 'ZIPCODE'])
    c = pd.merge(b, lane_data, how='left', on=['Year', 'ZIPCODE'])
    all_data  = pd.merge(c, sidewalk_data, how='left', on=['Year', 'ZIPCODE'])
    return all_data 

