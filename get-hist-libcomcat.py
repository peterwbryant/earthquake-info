import pandas as pd
from datetime import datetime
from libcomcat.dataframes import get_summary_data_frame
from libcomcat.search import search

# Lindsborg location, lat and long, degrees
centerLat = 38.5735
centerLong = -97.6745
# radius, km
radius = 100

# get events from libcomcat
summary_events = search(starttime=datetime(1994, 1, 17, 12, 30), endtime=datetime(2021, 12, 18, 12, 35),
                   maxradiuskm=radius, latitude=centerLat, longitude=centerLong)
sum_df = get_summary_data_frame(summary_events)

# rename magnitude
#sum_df.rename(columns={'magnitude': 'mag'}, inplace=True)

# Create new dataframe with only the data to save
#   convert to central time and make time the index
new_time_index = pd.DatetimeIndex(pd.to_datetime(sum_df['time'] )).tz_localize('UTC').tz_convert('US/Central')

longitude = sum_df['longitude'].to_numpy()
latitude = sum_df['latitude'].to_numpy()
magnitude = sum_df['magnitude'].to_numpy()
#location_st = sum_df['location'].to_numpy()

data_to_save = {'latitude':latitude, 'longitude':longitude, 'magnitude':magnitude}
eq_data = pd.DataFrame(data=data_to_save,
                       index=new_time_index)

# pickle it
eq_data.to_pickle('./historyDF.pkl')