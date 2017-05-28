# -*- coding: utf-8 -*-
"""
Created on Tue May 23 17:02:28 2017

@author: Edward Furey

Version: Python 2.7

This program plots airports and routes from the datasets at openflights.org
https://openflights.org/data.html
You need airports.dat (Airports only, high quality) and routes.dat

I also used earthmap_hires.jpg from
http://flatplanet.sourceforge.net/maps/natural.html

Python geographiclib is also required:
pip install geographiclib


"""

import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy.misc import imread

from geographiclib.geodesic import Geodesic

geod = Geodesic.WGS84
geod = Geodesic(6378388, 1/297.0) # the international ellipsoid

plt.style.use('ggplot')


def makemap(title):  # plot all the airports dots
    fig = plt.figure(figsize=(48,24))
    
    ax = fig.add_subplot(111)
    ax.set_title(title.decode('utf8'))
    ax.grid(b=False)
    for spine in ['left','right','top','bottom']:
        ax.spines[spine].set_color('k')
        
    img = imread("earthmap_hires.jpg")
    
    ax.imshow(img, extent=[-180, 180, -90, 90], zorder=0) #extent=[left, right, bottom, top]
    ax.set_xlim([-180,180])
    ax.set_ylim([-90,90])

    if plot_unused == True:
        """ Original color codes    
        ax.scatter(airstrips.Longitude, airstrips.Latitude, marker='.', color='#00ffff', s=5, zorder=1)
        ax.scatter(minors.Longitude, minors.Latitude, marker='.', color='#00ff00', s=5, zorder=2)
        ax.scatter(smalls.Longitude, smalls.Latitude, marker='.', color='#ffff00', s=10, zorder=3)
        ax.scatter(mediums.Longitude, mediums.Latitude, marker='.', color='#ff0000', s=20, zorder=4)
        ax.scatter(majors.Longitude, majors.Latitude, marker='.', color='#ff00ff', s=30, zorder=5)
        ax.scatter(intls.Longitude, intls.Latitude, marker='.', color='#0000ff', s=40, zorder=6)
        ax.scatter(topintls.Longitude, topintls.Latitude, marker='.', color='#000000', s=50, zorder=7)
        """
        ax.scatter(airstrips.Longitude, airstrips.Latitude, marker='.', color='#00ffff', s=5, zorder=1)
        ax.scatter(minors.Longitude, minors.Latitude, marker='.', color='#ffff00', s=5, zorder=2)
        ax.scatter(smalls.Longitude, smalls.Latitude, marker='.', color='#ff0000', s=10, zorder=3)
        ax.scatter(mediums.Longitude, mediums.Latitude, marker='.', color='#ff0000', s=20, zorder=4)
        ax.scatter(majors.Longitude, majors.Latitude, marker='.', color='#ff0000', s=30, zorder=5)
        ax.scatter(intls.Longitude, intls.Latitude, marker='.', color='#ff0000', s=40, zorder=6)
        ax.scatter(topintls.Longitude, topintls.Latitude, marker='.', color='#ff0000', s=50, zorder=7)
 
    return ax


def getWaypoints(oLat, oLong, dLat, dLong):
    wlongs = [oLong]
    wlats = [oLat]
    l = geod.InverseLine(oLat, oLong, dLat, dLong, Geodesic.LATITUDE | Geodesic.LONGITUDE)
    da = 1
    n = int(math.ceil(l.a13 / da))
    try:
        da = l.a13 / n
    except:
        print('error {} {} {}'.format(da, l.a13, n))
    for i in range(n + 1):
        a = da * i
        g = l.ArcPosition(a, Geodesic.LATITUDE | Geodesic.LONGITUDE) # | Geodesic.LONG_UNROLL)
        wlongs = wlongs + [g['lon2']]
        wlats = wlats + [g['lat2']]
    return wlongs, wlats

def plotPath(pLongs, pLats, col, al, zOrder):
    for i in range(len(pLongs)-1):
        if pLongs[i] - pLongs[i+1] > 180: # right side
            #print('jumping east'),
            ax.plot(pLongs[:i] + [pLongs[i+1]+360], pLats[:i+1], color=col, alpha=al, zorder=zOrder)
            pLongs = [pLongs[i] - 360] + pLongs[i+1:]
            pLats = pLats[i:]
            break
        if pLongs[i] - pLongs[i+1] < -180: # left side
            #print('jumping west'),
            ax.plot(pLongs[:i] + [pLongs[i+1]-360], pLats[:i+1], color=col, alpha=al, zorder=zOrder)
            pLongs = [pLongs[i] + 360] + pLongs[i+1:]
            pLats = pLats[i:]
            break
    ax.plot(pLongs, pLats, color=col, linewidth = 1.0, alpha=al, zorder=zOrder)
    ax.scatter(pLongs[-1], pLats[-1], marker='.', color='black', s=30, zorder=5)


""" Old straight vector distance
def vector(oLong, dLong, oLat, dLat):
    if oLong - dLong > 180: # right side
        length = math.sqrt((dLong+360-oLong)*(dLong+360-oLong) + (dLat-oLat)*(dLat-oLat))
    elif oLong - dLong < -180: # left side
        length = math.sqrt((dLong-360-oLong)*(dLong-360-oLong) + (dLat-oLat)*(dLat-oLat))
    else:
        length = math.sqrt((dLong-oLong)*(dLong-oLong) + (dLat-oLat)*(dLat-oLat))
    return length
"""

""" Old straight path plot
def plotSection(oLong, dLong, oLat, dLat, col, al, zOrder):
    if oLong - dLong > 180: # right side
        ax.plot([oLong, dLong + 360], [oLat, dLat], color=col, alpha=al, zorder=zOrder)
        ax.plot([oLong - 360, dLong], [oLat, dLat], color=col, alpha=al, zorder=zOrder)
    elif oLong - dLong < -180: # left side
        ax.plot([oLong, dLong - 360], [oLat, dLat], color=col, alpha=al, zorder=zOrder)
        ax.plot([oLong + 360, dLong], [oLat, dLat], color=col, alpha=al, zorder=zOrder)
    else:
        ax.plot([oLong, dLong], [oLat, dLat], color=col, alpha=al, zorder=zOrder)
    #ax.scatter(dLong, dLat, marker='.', color=col, s=40, zorder=zOrder)
"""

def createSizeColumn():
    for i, aAP in airports.iterrows():
        aID = aAP.AirportID
        try:
            in_ = len(routes[routes.DestinationAirportID == aID]) # count the incoming routes
        except:
            in_ = 0
        try:
            out = len(routes[routes.SourceAirportID == aID]) # count the outgoing routes
        except:
            out = 0
        #if (in_ + out) > 899: 
            print('index:{} AirportID:{} IATA:{} routes:{}'.format(i,aID,airports.loc[i].IATA,in_ + out))
        airports.set_value(i, 'Size', in_ + out)



"""
Start of main code
"""

print('Loading data.')
#airports = pd.read_csv('airports.dat', names=['AirportID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz', 'Type', 'Source', 'Size'], na_values=['\N','\\N'])
airports = pd.read_csv('airports2.dat')
routes = pd.read_csv('routes.dat', names=['Airline', 'AirlineID', 'SourceAirport', 'SourceAirportID', 'DestinationAirport', 'DestinationAirportID', 'Codeshare', 'Stops', 'Equipment'], na_values=['\N','\\N'])


airports.AirportID = airports.AirportID.astype("int32")
airports.Altitude = airports.Altitude.astype("int32")
airports.Size.fillna(0, inplace=True)
airports.Size = airports.Size.astype("int32")

routes.SourceAirportID.fillna(-1, inplace=True)
routes.DestinationAirportID.fillna(-1, inplace=True)
routes.SourceAirportID = routes.SourceAirportID.astype("int32")
routes.DestinationAirportID = routes.DestinationAirportID.astype("int32")


# comment this out if loading airports2.dat
#print('Calculating airport sizes.')
#createSizeColumn()

# uncomment this to save a new csv with the Size column
#airports.to_csv('airports2.dat',index=False)


# create the groups for dot size and color
airstrips = airports[airports.isnull().IATA] # airports with no IATA code
minors = airports[(airports.Size == 0) & (airports.IATA <> "")] # airports with no routes
smalls = airports[(airports.Size > 0) & (airports.Size < 10)]
mediums = airports[(airports.Size > 9) & (airports.Size < 50)]
majors = airports[(airports.Size > 49) & (airports.Size < 200)]
intls = airports[(airports.Size > 199) & (airports.Size < 900)]
topintls = airports[airports.Size > 899] # 20 = 709, 10 = 900 5 = 1000


# uncomment this and change IATA code to print map for particular airport
topintls = airports[airports.IATA == 'MEL'] # London LHR

plot_unused = False


"""
Create the maps
"""
print('Creating maps.')
exceptions = [-1] # a list of airports in routes.dat that don't appear in airports.dat
num = 1 # initial digit for file name
pdone = 0 # flag so parent airports are only processed once

if len(topintls) == 0:
    print('Invalid IATA code.')

for idx, intlAP in topintls.iterrows():
    # finals keeps track of final destinations, so each destination is only mapped using the most direct route. (could be optimised to take first trip length in to account)
    finals = pd.DataFrame([[intlAP.AirportID, intlAP.AirportID, 0.0]], columns = ['SID', 'DID', 'dist'])
    
    # DataFrame of the routes leaving this airport
    trips = routes[routes.SourceAirportID == intlAP.AirportID]
    #print('{} {}: {} trips'.format(intlAP.AirportID, intlAP.IATA, len(trips)))
    
    print('Processing {}: {}, {} routes.'.format(intlAP.IATA, airports[airports.AirportID == intlAP.AirportID].Name.values[0], len(trips)))
    
    # Add the earth background and populate the airports scatter dots
    ax = makemap(intlAP.Name)
    # Mark the origin airport
    ax.scatter(airports[airports.AirportID == intlAP.AirportID].Longitude.values[0], airports[airports.AirportID == intlAP.AirportID].Latitude.values[0], marker='.', color='black', s=40, zorder=10)
    
    """ find the first leg trips """
    for tID, trip in trips.iterrows():
        try:
            # try to get Long and Lat for this airport. Fails if AirportID in routes.dat doesn't exist in airports.dat
            destlong = airports[airports.AirportID == trip.DestinationAirportID].Longitude.values[0]
            destlat = airports[airports.AirportID == trip.DestinationAirportID].Latitude.values[0]
        except:
            exceptions.append(trip.DestinationAirportID)
            
        # Only process airports that are not on the exceptions list
        if not trip.DestinationAirportID in exceptions:
            # check if we have already processed this airport
            if trip.DestinationAirportID in finals.DID.values:
                # if we have processed it, get the index
                i = finals[(finals.DID == trip.DestinationAirportID)].index.tolist()[0]
                if finals.loc[i].dist == 0:
                    # already a parent, so already been processed
                    pdone = 1 # set to 1 so we skip further processing
                else: # promote the child airport to a parent airport, since it's a first leg trip it will never be a second leg destination
                    finals.loc[(finals['DID']==trip.DestinationAirportID)] = [[intlAP.AirportID,trip.DestinationAirportID, 0.0]]
                    pdone = 0 # set to 0 to proccess, since it's now a first leg destination
            else: # if we have not processed this airport before
                # add new parent trip (dist 0 ensures it won't be overwritten)
                newdf = pd.DataFrame([[intlAP.AirportID, trip.DestinationAirportID, 0.0]], columns = ['SID', 'DID', 'dist'])
                finals = finals.append(newdf, ignore_index=True)
                pdone = 0 # set to 0 to ensure this new parent airport is processed
                
            
            """ Process this airport """
            if pdone == 0: # if we haven't processed the child routes for this airport

                # plot the first leg route
                wLongs, wLats = getWaypoints(intlAP.Latitude, intlAP.Longitude, destlat, destlong)
                plotPath(wLongs, wLats, 'r', 0.5, 9)
                
                """ find sub trips """
                # get dataframe of all the child routes
                secLeg = routes[routes.SourceAirportID == trip.DestinationAirportID]
                
                #print('{} has {} children.'.format(airports[airports.AirportID == trip.DestinationAirportID].IATA.values[0], len(secLeg)))
                print('{} '.format(airports[airports.AirportID == trip.DestinationAirportID].IATA.values[0])),
    
                # iterate through child routes
                for stID, strip in secLeg.iterrows():
                        if not strip.DestinationAirportID in exceptions:
                            try:
                                # try to get Long and Lat for this airport. Fails if AirportID in routes.dat doesn't exist in airports.dat
                                sdestlong = airports[airports.AirportID == strip.DestinationAirportID].Longitude.values[0]
                                sdestlat = airports[airports.AirportID == strip.DestinationAirportID].Latitude.values[0]
                            except:
                                exceptions.append(strip.DestinationAirportID)
                                
                        if not strip.DestinationAirportID in exceptions: # if we made it through the Long/Lat lookups
                            # get the distance to the child airport (could improve by including first leg distance here)                        
                            newdist = geod.Inverse(destlat, destlong, sdestlat, sdestlong)['s12'] #vector(destlong, sdestlong, destlat, sdestlat)
                            #print('Checking child {}: '.format(strip.DestinationAirportID)),                 
                            if strip.DestinationAirportID in finals.DID.values:
                                # if we have already added this child, get the index
                                i = finals[(finals.DID == strip.DestinationAirportID)].index.tolist()[0]
                                # if the new distance to the child is shorter than the old one (improved route)
                                if finals.loc[i].dist > newdist:
                                    # update the child with the new parent airport and distance
                                    #print('updating child')
                                    finals.loc[(finals['DID']==strip.DestinationAirportID)] = [[trip.DestinationAirportID, strip.DestinationAirportID, newdist]]
                                else:
                                    pass # pass does nothing except make the indent so the else doesn't fail
                                    #print('OK') # current child still the best
                            else:
                                #print('Adding new child')
                                newdf = pd.DataFrame([[trip.DestinationAirportID, strip.DestinationAirportID, newdist]], columns = ['SID', 'DID', 'dist'])
                                finals = finals.append(newdf, ignore_index=True)
                                

    print
    print('{} destinations.'.format(len(finals)-1)) # -1 because the origin airport doesn't count as a destination
    #print('{} exceptions.'.format(len(exceptions)))

    """ plot the second leg routes """
    print('Plotting routes...')
    for i, splot in finals.iterrows():
        #print('{} '.format(airports[airports.AirportID == splot.DID].IATA.values[0])),
        if splot.dist > 0:
            olong = airports[airports.AirportID == splot.SID].Longitude.values[0]
            olat = airports[airports.AirportID == splot.SID].Latitude.values[0]
            dlong = airports[airports.AirportID == splot.DID].Longitude.values[0]
            dlat = airports[airports.AirportID == splot.DID].Latitude.values[0]
            wLongs, wLats = getWaypoints(olat, olong, dlat, dlong)
            plotPath(wLongs, wLats, 'orange', 0.5, 8)

    print('Saving file... '),
    plt.savefig(str(num) + ' ' + intlAP.Name + ".png", bbox_inches='tight', dpi=106)
    print('Done.')
    print
    num = num + 1


print('All airport maps completed.')

"""
End of code
"""
    
    
