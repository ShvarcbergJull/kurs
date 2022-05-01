#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 12:52:47 2018

@author: Artem Vesnin (remake of original Sergey Voeykov's C++ code)
"""

from numpy import pi, sin, cos, exp
from gcd import great_circle_distance as dlarc

RE_meters = 6671000.

class Ring:
    
    """
    The model for ring disturbance. Assume it starts from ring source with 
    center at (lat, lon) and radius r0. Be carefull with units.
    Fields:
        lat, lon: double
            source coordinates of the disturbance (radians)
        t0: double
            disturbance start time (hours)
        r0: double
            source initial radius (meters)
        t_rise: double
            time for disturbance to fully develop, i.e. time of amplitude 
            growth (hours)
        t_dump: double
            time to disturbance amplitude drop to zero (hours)
        envelope_scale: double
            the disturbance encvelope width in propagation direction, 6*sigma 
            for gaussian (meters). Small scale irregularities can be written 
            inside envelope (see wavelength field). 
        amplitude: double 
            amplitude of disturbance in percents from background (percent)
        v_group, v_phase: double
            group and phase velocity for disturbance (wave packet) propagation
            (meters/seconds)
        wavelength: double
            wavelength of the small scale irregularities inside envelope
            (meters)
    """
    def __init__(self):
        self.lat = 0.
        self.lon = 0.
        self.t0 = 0.
        self.r0 = 0.
        self.t_rise = 0.
        self.t_damp = 0.
        self.envelope_scale = 0.
        self.amplitude = 0.
        self.v_group = 0.
        self.v_phase = 0.
        self.wavelength = 0.
        self.initial_phase = 0.
        pass
    
    def get_disturbed_ne(self, ut, lat, lon):
        """
        Gives disturbed Ne for (lat, lon) and UT for given Ring parameters
        Parameters:
            ut: double
                universal time in hours
            lat, lon: double 
                latitude and longitude in radians 
            rings: list of Ring
                Ring TIDs which make disturbed Ne
        """
        ut_sec = ut * 3600.
        
        k_time = 0.
        exp_arg = 0.
        
        t_start = self.t0 * 3600.
        t_rise = self.t_rise * 3600
        t_damp = self.t_damp * 3600
        t_fin = t_start + t_rise + t_damp
        if ut_sec < t_start or ut_sec > t_fin:
            return 0
        
        R = dlarc(lat, lon, self.lat, self.lon, RE_meters)
        if R < self.r0 or R > (t_rise + t_damp) * self.v_group:
            return 0

        if ut_sec < t_start + t_rise:
            k_time = (1. - cos((ut_sec-t_start)*pi/t_rise))/2.;
        else:
            exp_arg = (ut_sec - t_start - t_rise)*3./t_damp
            k_time = exp(-exp_arg**2/2.)

        exp_arg = (R - self.r0 - self.v_group*(ut_sec-t_start))*6.
        exp_arg /= self.envelope_scale
        k_env = self.amplitude * exp(-exp_arg**2/2.)
        omega = 2.*pi * self.v_phase/self.wavelength
        k_sin = sin(omega*(ut_sec - t_start - (R-self.r0)/self.v_phase) + 
                    self.initial_phase)
        total_disturbtion = k_time * k_env * k_sin
        total_disturbtion = total_disturbtion if total_disturbtion < 1 else 1
        total_disturbtion = total_disturbtion if total_disturbtion > -1 else -1
        return total_disturbtion




