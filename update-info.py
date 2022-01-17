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

magnitude = df_filtered['mag'].to_numpy()
location_st = df_filtered['place'].to_numpy()
url_st = ['Not available as of posting'] * len(magnitude)

info_to_update = {'magnitude':magnitude, 'location':location_st, 'USGS event page':url_st, 'USGS event page raw':url_st}
eq_info_new = pd.DataFrame(data=info_to_update,
                       index=time_index)

# read previously saved history file
info_df = pd.read_pickle('infoDF.pkl')

# merge new info with old
#   Merge gets confused with updated info from the libcomcat entries,
#   so choose only events that have a timestamp after previously stored events
# TODO see if there is a delta needed here to minimize duplicate events
eq_info_new = eq_info_new.loc[eq_info_new.index > info_df.index[-1]]
newdf = pd.concat([info_df, eq_info_new]).sort_values(by=['time'])

# replace history file
newdf.to_pickle('./infoDF.pkl')

# write html table
timeOnly = newdf.index.round('S').map(lambda t: t.strftime('%H:%M:%S')).to_numpy()

newdf = newdf.assign(tempTime=timeOnly)
newdf.index = newdf.index.round('S').map(lambda t: t.strftime('%Y-%m-%d'))
newdf.reset_index(inplace=True)
newdf.rename(columns={'time':'date', 'tempTime':'time (US Central)'}, inplace=True)
newdf = newdf[['date', 'time (US Central)', 'magnitude', 'location', 'USGS event page']]

# escape=False to write < and > correctly in output file
pd.set_option('colheader_justify', 'center')

html_string = '''
<html>
  <head><title>30 Most Recent Events within 100 km</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    {table}
  </body>
</html>.
'''
with open('eq-table.html', 'w') as f:
    f.write(html_string.format(table=newdf[-30:].sort_index(ascending=False).to_html(classes='mystyle', index=False, escape=False)))