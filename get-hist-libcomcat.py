import pandas as pd
from datetime import datetime
from libcomcat.dataframes import get_summary_data_frame
from libcomcat.search import search

# Lindsborg location, lat and long, degrees
centerLat = 38.5735
centerLong = -97.6745
# radius, km
radius = 30

# get events from libcomcat
summary_events = search(starttime=datetime(1994, 1, 17, 12, 30), endtime=datetime(2021, 12, 18, 12, 35),
                   maxradiuskm=radius, latitude=centerLat, longitude=centerLong)
sum_df = get_summary_data_frame(summary_events)

# rename magnitude
sum_df.rename(columns={'magnitude': 'mag'}, inplace=True)

# pickle it
sum_df.to_pickle('./historyDF.pkl')