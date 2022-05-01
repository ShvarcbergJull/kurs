#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 12:36:59 2017

@author: Artem Vesnin (remake of original Sergey Voeykov's C++ code)
"""

import numpy as np
from numpy import sin, cos, radians, arcsin, arccos, sqrt, degrees, exp
from numpy import abs as fabs


def sun_zenith(yday, UT, lat, lon):
    B = radians((yday-81)*360./365.)
    delta = radians(23.45*sin(B))
    EoT = (9.87*sin(2.*B) - 7.53*cos(B) - 1.5*sin(B))/60.
    LT = UT + degrees(lon)/15.
    if LT >= 24.:
        LT -= 24.
    hra = radians(15.*(LT + EoT - 12.))

    sin_el = sin(delta)*sin(lat) + cos(delta)*cos(lat)*cos(hra)
    el = arcsin(sin_el)
    el = np.pi/2. - el
    return el

def get_ne(yday, UT, lat, lon, z, night = 0.2, sigma = 0.819963, **kwargs):
    """
    Return electron concentration for given parameters
        
    Parameters:
        yday - day of year
        UT - universal time
        lat, lon, z - latitude, longitude adn heights of the point of interest        
        ne_0 - max concentration
        hmax - max height
        half_thickness - slab thickness of the ionosphere
        tids - models of ionosperic ditirbtions
    """
    ne_0 = kwargs["ne_0"]
    hm = kwargs["hmax"]
    b0 = kwargs["half_thickness"]
    
    zenith = sun_zenith(yday, UT, lat, lon)
    z_dep = -2.*(z-hm)/b0
    ne = exp(z_dep)/(night + (1 - night) * exp(-zenith ** 2)/(2 * sigma ** 2))
    
    disturbed_ne = get_total_disturbed_ne(UT, lat, lon, **kwargs)
    ne = ne_0 * exp(0.5 * (1 + z_dep - ne))
    ne = ne * (1 + disturbed_ne)
    return ne

def get_total_disturbed_ne(ut, lat, lon, **kwargs):
    if "tids" not in kwargs:
        return 0
    disturbed_ne = 0
    for tid in kwargs["tids"]:
        disturbed_ne += tid.get_disturbed_ne(ut, lat, lon)    
    return disturbed_ne
    

def get_tec(yday, UT, az, el, lat_0, lon_0, **kwargs):
    """
    Returns tec for given input parameters
    
    Parameters:
        yday - day of year
        UT - universal time
        az, el - azimuth and elevation
        lat, lon - latitude and longitude of the origin        
        z_start, z_end - start and end height
        l_step - step along the ray
    """
    Rz = 6371.
    TEC = 0.
    el = degrees(el)
    az = degrees(az)
    z_start = kwargs["z_start"]
    z_end = kwargs["z_end"]
    l_step = kwargs["l_step"]
    colat = np.pi/2 - lat_0
    cos_q = cos(radians(el))
    sin_q = sin(radians(el))
    B = radians(360. - az) if az>180. else radians(az)
    cosB = cos(B)
    sinB = sin(B)
    get_lon = lambda az, lon0, A: lon_0 + A if az < 180 else lon_0 - A
    get_b = lambda psi : arccos(cos(psi)*cos(colat)+sin(psi)*sin(colat)*cosB)
    if fabs(cos_q) < 1e-10: # vartical ray condition, do not happens usually
        ne_prev = get_ne(yday,UT,lat_0,lon_0,z_start, **kwargs)
        z = z_start
        while z < z_end:
            z += l_step
            ne = get_ne(yday,UT,lat_0,lon_0,z, **kwargs)
            TEC += (ne + ne_prev)*l_step*1000./2.
            ne_prev = ne
    else:
        sin_ksi = Rz*cos_q/(Rz + z_start)
        ksi = arcsin(sin_ksi)
        psi = np.pi/2. - ksi - radians(el)      
        l_start = sin(psi)*Rz/sin_ksi 
        b = get_b(psi)
        LAT = np.pi - b
        A = arcsin(sin(psi)*sinB/sin(b))
        LON = get_lon(az, lon_0, A)
        ne_prev = get_ne(yday,UT,LAT,LON,z_start, **kwargs)
    
        l_cur = l_start
        z = z_start   
        while z < z_end:
            l_cur += l_step
            z = sqrt(Rz**2 + l_cur**2 + Rz*l_cur*sin_q) - Rz
            psi = arcsin(l_cur*cos_q/(Rz+z)) 
            b = get_b(psi)
            LAT = np.pi - b
            A = arcsin(sin(psi)*sinB/sin(b))
            LON = get_lon(az, lon_0, A)
            ne = get_ne(yday,UT,LAT,LON,z, **kwargs)
            TEC += (ne+ne_prev)*l_step*1000./2.
            ne_prev = ne
    return TEC/1e16