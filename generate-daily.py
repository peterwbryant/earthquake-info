import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from eqUtils import *
# mapping imports
import os
os.environ["PROJ_LIB"]='~/anaconda3/envs/earthquake-libcomcat/share/'
from mpl_toolkits.basemap import Basemap
import geopandas as gpd

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
hdf = pd.read_pickle('historyDF.pkl')

# merge new data with old
#   merge with how='outer' for union
hist_df = pd.merge(hdf, eq_data_new, on=['time','latitude','longitude','magnitude'], how='outer')

# replace history file
hist_df.sort_values(by=['time']).to_pickle('./historyDF.pkl')

# Process and generate plots -------------------------------------------------
#  Map
kansas = gpd.read_file('mapfiles/tl_2017_20_place.shp')

plotlat = hist_df['latitude'].to_numpy()
plotlong = hist_df['longitude'].to_numpy()
plotmag = hist_df['magnitude'].to_numpy()

fig_map = plt.figure(figsize=(10, 10))
fig_map.patch.set_alpha(0.0)
m = Basemap(projection='lcc', resolution='h',
            lat_0=38.5735, lon_0=-97.6745,
            width=1.05E6, height=1.2E6)
m.shadedrelief()
m.drawstates(linewidth=2)
m.drawcounties()
m.drawrivers(color='aqua', linewidth=1.3)

# extent in lat/lon (dec degrees)
ulx = -103
uly = 41
lrx = -93
lry = 36

# transform coordinates to map projection
xmin, ymin = m(ulx, lry)
xmax, ymax = m(lrx, uly)

# set the axes limits
ax = plt.gca()
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# add events
m.scatter(plotlong, plotlat, latlon=True,
          c=plotmag, s=100,
          cmap='YlOrRd', alpha=0.5)

# create colorbar
cb = plt.colorbar()
cb.set_label(label=r'Magnitude', size=18)
cb.ax.tick_params(labelsize=16)
plt.clim(plotmag.min(), plotmag.max())

# lindsborg
x,y = m(-97.6745,38.5735)
plt.plot(x,y, 'ok', markersize=5)
plt.text(x+10000,y+10000,'Lindsborg', fontsize=13)

fig_map.tight_layout()
fig_map.savefig('eq-map.png', dpi=400);

# -----------------------------------------------------------------------
#  Time History
# magnitude time history
x = mdates.date2num(hist_df.index)
y = hist_df['magnitude']

# rolling count
day_count_df = hist_df.groupby(hist_df.index.date).count()
day_count_df.index = pd.to_datetime(day_count_df.index)
repop_dates = pd.date_range(start=day_count_df.index[0], end=day_count_df.index[-1], freq='1D')
day_count_df = day_count_df.reindex(repop_dates, fill_value=0)
rolling_count = day_count_df.rolling('30d').sum()
year_count = day_count_df.rolling('365d').sum()

x2 = mdates.date2num(rolling_count.index)
y2 = rolling_count['magnitude']

y3 = year_count['magnitude']

# plot
fig, host = plt.subplots(figsize=(8,6))
fig.patch.set_alpha(0.0)
rt_ax = host.twinx()
rt_ax2 = host.twinx()

host.set_ylabel('Magnitude [ML]', size=16)
rt_ax.set_ylabel('365 day rolling total', size=16)
rt_ax2.set_ylabel('30 day rolling total', size=16)

p3, = rt_ax2.plot_date(x2, y2, ':', color='dimgrey')
p2, = rt_ax.plot_date(x2,y3, '-', color='maroon')
p1, = host.plot_date(x,y)

rt_ax2.spines['right'].set_position(('outward', 60))

host.yaxis.label.set_color(p1.get_color())
rt_ax.yaxis.label.set_color(p2.get_color())
rt_ax2.yaxis.label.set_color(p3.get_color())

plt.gcf().autofmt_xdate()

host.tick_params(axis='both', labelsize=14)
rt_ax.tick_params(axis='y', labelsize=14)
rt_ax2.tick_params(axis='y', labelsize=14)

plt.title('Earthquakes within 100 km of Lindsborg\n$\it{updated}$ '+datetime.today().strftime('%Y-%m-%d'), size=20)
plt.grid()

fig.tight_layout()
fig.savefig('eq-time-hist-2ax.png', dpi=400);
