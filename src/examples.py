from scenario import Scenario
from team import Team
from league import League
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
import statsmodels.api as sm

# Team class examples

# retrieves all the gambling data specified in the Team Class for the Celtics
celtics_data = Team("Celtics")

# retrieves all the gambling data for the Celtics in the 2018 season
celtics_2018_season_data = Team("Celtics", season='2018')

# retrieves all the gambling data for the Celtics between 1/10/2017 - 11/11/2018. 
# DATES MUST BE IN YYYY-MM-DD FORMAT
celtics_range_data = Team("Celtics", start_date='2017-1-10', end_date='2018-11-11')

# retrieves all the gambling data for the Celtics between 1/1/2015 - 11/11/2018. 
# DATES MUST BE IN YYYY-MM-DD FORMAT
celtics_range_data_no_start_date_specified = Team("Celtics", end_date='2016-11-11')

# retrieves all the gambling data for the Celtics 11/11/2018 - their latest game 
# DATES MUST BE IN YYYY-MM-DD FORMAT
celtics_range_data_no_end_date_specified = Team("Celtics", start_date='2018-11-11')


# Scenario class examples

# retrieves all the gambling data specified in the Team Class for the Celtics
celtics_data = Team("Celtics")

# retrieves all the gambling data for the Celtics in the 2018 season
celtics_2018_season_data = Team("Celtics", season='2018')

# retrieves all the gambling data for the Celtics between 1/10/2017 - 11/11/2018. 
# DATES MUST BE IN YYYY-MM-DD FORMAT
celtics_range_data = Team("Celtics", start_date='2017-1-10', end_date='2018-11-11')

# retrieves all the gambling data for the Celtics between 1/1/2015 - 11/11/2018. 
# DATES MUST BE IN YYYY-MM-DD FORMAT
celtics_range_data_no_start_date_specified = Team("Celtics", end_date='2016-11-11')

# retrieves all the gambling data for the Celtics 11/11/2018 - their latest game 
# DATES MUST BE IN YYYY-MM-DD FORMAT
celtics_range_data_no_end_date_specified = Team("Celtics", start_date='2018-11-11')


