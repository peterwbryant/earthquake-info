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
summary_events = search(starttime=datetime(2014, 1, 17, 12, 30), endtime=datetime.now(),
                   maxradiuskm=radius, latitude=centerLat, longitude=centerLong)
sum_df = get_summary_data_frame(summary_events)

# Create new dataframe with only the data to save
#   convert to central time and make time the index
new_time_index = pd.DatetimeIndex(pd.to_datetime(sum_df['time'] )).tz_localize('UTC').tz_convert('US/Central')

# data table
longitude = sum_df['longitude'].to_numpy()
latitude = sum_df['latitude'].to_numpy()
magnitude = sum_df['magnitude'].to_numpy()

# info table
location_st = sum_df['location'].to_numpy()
url_st = sum_df['url'].to_numpy()

data_to_save = {'latitude':latitude, 'longitude':longitude, 'magnitude':magnitude}
eq_data = pd.DataFrame(data=data_to_save,
                       index=new_time_index)

info_to_save = {'magnitude':magnitude, 'location':location_st, 'USGS event page':url_st}
eq_info = pd.DataFrame(data=info_to_save,
                       index=new_time_index)

# pickle them
eq_data.to_pickle('./historyDF.pkl')
eq_info.to_pickle('./infoDF.pkl')