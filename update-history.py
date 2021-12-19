import pandas as pd
from eqUtils import *

# new data from usgs
df = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')

# Filter new events by location
#   radius, km  -- 100 km is currently the radius in the libcomcat query
radius = 100
# lindsborg -- currently used in libcomcat query
centerLat = 38.5735
centerLong = -97.6745

df_filtered = df.loc[gcDistpd(centerLat, centerLong, df)<= radius]

# new index to match history, central time
time_index = pd.DatetimeIndex(pd.to_datetime(df_filtered['time'] )).tz_convert("US/Central")

longitude = df_filtered['longitude'].to_numpy()
latitude = df_filtered['latitude'].to_numpy()
magnitude = df_filtered['mag'].to_numpy()

data_to_update = {'latitude':latitude, 'longitude':longitude, 'magnitude':magnitude}
eq_data_new = pd.DataFrame(data=data_to_update,
                       index=time_index)


# read previously saved history file
hist_df = pd.read_pickle('historyDF.pkl')

# merge new data with old
#   merge with how='outer' for union
newdf = pd.merge(hist_df, eq_data_new, on=['time','latitude','longitude','magnitude'], how='outer')

# replace history file
newdf.sort_values(by=['time']).to_pickle('./historyDF.pkl')