import numpy as np
import geopandas as gpd


url_list = [
 'https://opendata.arcgis.com/datasets/7015d5d46a284f94ac05c2ea4358bcd7_0.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/5fc63b2a48474100b560a7d98b5097d7_1.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/27af9a2485c5442bb061fa7e881d7022_2.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/4f62515558174f53979b3be0335004d3_3.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/29f801d03c9b4b608bca6a8e497278c3_4.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/a0019dd0d6464747a88921f5e103d509_5.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/40bcfbc4054549ebba8b5777bbdd40ff_6.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/16cedd233d914118a275c6510115d466_7.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/902fd604ecf54adf8579894508cacc68_8.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/170b764c52f34c9497720c0463f3b58b_9.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/2c37babc94d64bbb938a9b520bc5538c_10.geojson',  # noqa: E501
 'https://opendata.arcgis.com/datasets/a35aa9249110472ba2c69cc574eff984_11.geojson']  # noqa: E501


def get_gdf(year):
    '''Enter the desired year to download the traffic flow count
    data for that year. Example: enter '7' for the year 2007.
    '''

    # Pulls the data from Seattle's open GIS.
    num = year-7
    gdf_year = gpd.read_file(url_list[num])
    # There are some inconsistencies in the
    # names of columns across years in this data,
    # so these conditional statements make everything the same.
    if year == 11:
        gdf_year = gdf_year.rename(columns={"YEAR_": 'YEAR'})
        gdf_year = gdf_year[gdf_year.STNAME != '16TH AVE S']
    if year == 12:
        gdf_year = gdf_year.rename(columns={'STDY_YEAR': 'YEAR'})
    if year == 15 or year == 16:
        gdf_year = gdf_year.rename(columns={"COUNTAAWDT": 'AAWDT',
                                            "FLOWSEGID": "GEOBASID",
                                            'FIRST_STNAME_ORD': 'STNAME'})
        gdf_year = gdf_year[['AAWDT', 'GEOBASID', 'STNAME',
                             'SHAPE_Length', 'geometry']]
        if year == 15:
            year_list = [2015]*len(gdf_year)
            gdf_year['YEAR'] = year_list
        elif year == 16:
            year_list = [2016]*len(gdf_year)
            gdf_year['YEAR'] = year_list
    elif year == 17 or year == 18:
        gdf_year = gdf_year.rename(columns={"AWDT": 'AAWDT',
                                            "FLOWSEGID": "GEOBASID",
                                            'STNAME_ORD': 'STNAME'})
        gdf_year = gdf_year[['AAWDT', 'GEOBASID',
                             'STNAME', 'SHAPE_Length',
                             'geometry']]
        if year == 17:
            year_list = [2017]*len(gdf_year)
            gdf_year['YEAR'] = year_list
        elif year == 18:
            year_list = [2018]*len(gdf_year)
            gdf_year['YEAR'] = year_list
    # This cleans the output to contain only relevant columns.
    gdf_year = gdf_year[['YEAR', 'AAWDT', 'GEOBASID',
                         'STNAME', 'SHAPE_Length',
                         'geometry']]
    # This removes any null values from the dataset.
    gdf_year = gdf_year[gdf_year.YEAR != 0]
    gdf_year = gdf_year[gdf_year.YEAR.notnull()]
    return gdf_year


def get_agg_year():
    year_list = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    agg_year_data = gpd.GeoDataFrame()
    for year in year_list:
        agg_year_data = agg_year_data.append(get_gdf(year))
    return agg_year_data


def test_plot_zip_traffic_data(year):
    inputs = list(range(7, 19))
    years = list(range(2007, 2019))
    year_dict = dict(zip(inputs, years))

    gdf_year = get_gdf(year)
    year_test = gdf_year['YEAR'].unique().astype(int)[0]

    assert year_dict.get(year) == year_test, 'Function downloaded incorrect year data'  # noqa: E501
    return


def test_plot_traffic_data_over_time():
    agg_year_data = get_agg_year()
    year_expect = np.array(range(2007, 2019))
    year_prod = agg_year_data['YEAR'].unique()
    assert np.array_equal(year_prod, year_expect), 'Aggregation of data by year did not occur correctly'  # noqa: E501
    return
