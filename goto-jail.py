# -*- coding: utf-8 -*-
"""
This script calls USGS structures endpoint for a file of polygon coordinates. Writes output to a file.
Does this by creating a POST request with proper layers and user-supplied coords.

@author: Robert Streetman
07-16-2017
"""
import requests
import json

#Format the coordinates here
def createPostData(coordinates):
    postdata = {'f':'geojson','inSR':'4326','outSR':'4326','geometryPrecision':'7','spatialRel':'esriSpatialRelIntersects','geometryType':'esriGeometryPolygon'}
    #USGS service requries non-conforming 'geojson' format
    geom = '{"rings":[' + coordinates + '],"spatialReference":{"wkid" : 4326}}'
    postdata.update({'geometry': geom})
    return postdata
    
#Change URLs/file names here
urlle = 'https://services.nationalmap.gov/arcgis/rest/services/structures/MapServer/9/query'
urljail = 'https://services.nationalmap.gov/arcgis/rest/services/structures/MapServer/11/query'
urlairport = 'https://services.nationalmap.gov/arcgis/rest/services/transportation/MapServer/34/query'
urlrail = 'https://services.nationalmap.gov/arcgis/rest/services/transportation/MapServer/42/query'
infilename = 'coordinates.txt'
outfilename = 'jail.txt'

print 'Reading input file...'
inputfile = open(infilename,'r')
outputfile = open(outfilename,'w')

#Each polygon needs to be on its own line
for polyCount, coordLine in enumerate(inputfile):
    outputfile.write('Polygon {}\n'.format(polyCount + 1))
    #Both requests use the same parameters
    dataDict = createPostData(coordLine)
    jailResp = requests.post(urljail, data=dataDict)
    
    #Prison request logic
    if jailResp.status_code == requests.codes.ok:
        outputfile.write('Prisons - Polygon {}\n'.format(polyCount + 1))
        jsonObj = json.loads(jailResp.text)
        
        for element in jsonObj['features']:
            outputfile.write('\t{}\t{}\n'.format(element['properties']['NAME'], element['geometry']['coordinates']))
    #These services are down A LOT, not my fault...
    elif jailResp.status_code == requests.codes['service_unavailable'] or jailResp.status_code == requests.codes['bad_gateway']:
        print 'Prison service unavailable due to server error (HTTP Response {})...'.format(jailResp.status_code)
    #This may have been my fault...    
    else:
        print 'Prison service request failed (HTTP Response {})...'.format(jailResp.status_code)
        
    outputfile.write('\n')
    leResp = requests.post(urlle, data=dataDict)
    
    #Police request logic
    if leResp.status_code == requests.codes.ok:
        outputfile.write('Police - Polygon {}\n'.format(polyCount + 1))
        jsonObj = json.loads(leResp.text)
        
        for element in jsonObj['features']:
            outputfile.write('\t{}\t{}\n'.format(element['properties']['NAME'], element['geometry']['coordinates']))
    #These services are down A LOT, not my fault...
    elif leResp.status_code == requests.codes['service_unavailable'] or leResp.status_code == requests.codes['bad_gateway']:
        print 'Police service unavailable due to server error (HTTP Response {})...'.format(leResp.status_code)
    #This may have been my fault...
    else:
        print 'Police service request failed (HTTP Response {})...'.format(leResp.status_code)
        
    outputfile.write('\n')
    airResp = requests.post(urlairport, data=dataDict)
    
    #Airport request logic
    if airResp.status_code == requests.codes.ok:
        outputfile.write('Airport - Polygon {}\n'.format(polyCount + 1))
        jsonObj = json.loads(airResp.text)
        
        for element in jsonObj['features']:
            outputfile.write('\t{}\t{}\n'.format(element['properties']['NAME'], element['geometry']['coordinates']))
    #These services are down A LOT, not my fault...
    elif airResp.status_code == requests.codes['service_unavailable'] or airResp.status_code == requests.codes['bad_gateway']:
        print 'Airport service unavailable due to server error (HTTP Response {})...'.format(airResp.status_code)
    #This may have been my fault...
    else:
        print 'Airport service request failed (HTTP Response {})...'.format(airResp.status_code)
        
    outputfile.write('\n')

inputfile.close()
outputfile.close()
print 'Done...'