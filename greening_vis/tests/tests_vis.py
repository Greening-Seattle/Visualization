import numpy as np

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
