import plotting_functions
from plotting_functions import get_gdf

def year_type(year):
    """
    This function checks that the
    year type is an integer 
    """
    if isinstance(year, int):
        print('Year is an Integer')
    else:
        raise Exception('TypeError', 'Year input is not an integer')
    return

def year_check (year):
    """
    Checks that the user has correctly 
    input a year in the dataset from 11 
    to 18 for the corresponding years
    """
    if  11 <= year_input <= 18:
        print('Valid Year Input')
    else:
        raise Exception('ValueError', 'gdf_year input not between 7 and 18')
    return
    

    
