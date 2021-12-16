import math
import numpy as np

# This is from sites about great circle distances:
#   - http://edwilliams.org/avform147.htm
#   - https://en.wikipedia.org/wiki/Great-circle_distance

def gcDist(centerLat, centerLong, ptLat, ptLong):
    '''Function to return great circle distance on earth, given center lat and long, point lat and long, all in degrees '''
    # go to radians
    cLat = centerLat * math.pi / 180.0
    cLong = centerLong * math.pi / 180.0
    pLat = ptLat * math.pi / 180.0
    pLong = ptLong * math.pi / 180.0

    # radius of earth, km
    rad = 6371.0

    # great circle formula
    dLambda = cLong - pLong
    dPhi = cLat - pLat

    drad = 2.0 * math.asin(math.sqrt( math.sin(dPhi/2.0)**2 + (1.0 - math.sin(dPhi/2.0)**2 - (math.sin((cLat+pLat)/2.0)**2) ) * (math.sin(dLambda/2.0)**2)  ) )

    # distance
    return drad * rad

def gcDistpd(centerLat, centerLong, dataFile):
    '''Function to return great circle distance on earth, given center lat and long, datafile with point lat and long, all in degrees '''
    # go to radians
    cLat = np.full(len(dataFile), centerLat * math.pi / 180.0)
    cLong = np.full(len(dataFile),centerLong * math.pi / 180.0)
    pLat = (dataFile['latitude'] * math.pi / 180.0).to_numpy()
    pLong = (dataFile['longitude'] * math.pi / 180.0).to_numpy()

    # radius of earth, km
    rad = 6371.0

    # great circle formula
    dLambda = cLong - pLong
    dPhi = cLat - pLat

    drad = 2.0 * np.arcsin(np.sqrt( np.sin(dPhi/2.0)**2 + (1.0 - np.sin(dPhi/2.0)**2 - (np.sin((cLat+pLat)/2.0)**2) ) * (np.sin(dLambda/2.0)**2)  ) )

    # distance
    return drad * rad