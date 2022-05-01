from numpy import sin, cos, arccos, pi, arcsin

RE_meters = 6371000

def great_circle_distance(late, lone, latp, lonp, R=RE_meters):
    """
    Calculates arc length
    late, latp: double
        latitude in radians
    lone, lonp: double
        longitudes in radians
    R: double
        radius
    """
    if lone < 0:
        lone += 2*pi
    if lonp < 0:
        lonp += 2*pi

    dlon = lonp - lone
    if dlon > 0.:
        if dlon > pi:
            dlon = 2 * pi - dlon
        else:
            pass
    else:
        if dlon < -pi:
            dlon += 2 * pi
        else:
            dlon = -dlon

    cosgamma = sin(late) * sin(latp) + cos(late) * cos(latp) * cos(dlon)
    return R * arccos(cosgamma)

#great_circle_distance(0.10, 0.10, 0.10, 0.10)