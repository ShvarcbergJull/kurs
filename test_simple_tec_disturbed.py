#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 13:53:49 2018

@author: Artem Vesnin
"""

import numpy as np
import datetime as dt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from tid_circle import Ring
import simple_tec as st

ring = Ring()
ring.lat = np.pi / 3
ring.lon = 0.
ring.t0 = 2.
ring.r0 = 250.
ring.t_rise = 0.25
ring.t_damp = 10.
ring.envelope_scale = 3500000.
ring.amplitude = 0.30
ring.v_group = 800
ring.v_phase = 600
ring.wavelength = 3500000


lat_step = 5
lon_step = 5
lat_range = list(range(-90, 90 + lat_step, lat_step))
lon_range = list(range(-180, 180, lon_step))  # no + lon_step since -180 and 180 is the same
data = np.zeros([len(lat_range) * len(lon_range), 4])
i = 0

tids = [ring]
for lat in lat_range:
    for lon in lon_range:
        kargs = {"z_start": 80, "z_end": 1000, "l_step": 10,
                 "ne_0": 2e12, "hmax": 300, "half_thickness": 100,
                 "tids": tids # comment this to remove ring disturbance
                 }
        d = st.get_tec(yday=1, UT=5.5, az=0, el=np.pi / 2,
                       lat_0=np.radians(lat), lon_0=np.radians(lon),
                       **kargs)
        data[i] = [lon, lat, 0, d]
        i += 1

np.save("map_disturbed.points", data)
lats = data[:, 1]
lons = data[:, 0]
vals = data[:, 3]

plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.scatter(lons, lats, c=vals)
ax.coastlines()
plt.show()

