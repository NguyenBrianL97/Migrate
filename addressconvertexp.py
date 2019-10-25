import requests, json, csv
import heapq
import re
firstcol=[]
secondcol=[]
thirdcol=[]
listoflat=[]
listoflon=[]
drivernumber=[]
drivername=[]
driveramount=[]
drivercounter=0
pickups=[]

time=[]
distances = []

f= open("carpools.txt","w+")
f.write("Carpools by Brian Loc Nguyen \n \n")

from pprint import pprint

with open('Hardy.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        #print row
        text = row[0]
        text2= row[1]
        text3=row[2]
        firstcol.append(text)
        secondcol.append(text2)
        thirdcol.append(text3)
        if row[1]=='Y':
            drivernumber.append(drivercounter)
            drivername.append(text3)
            driveramount.append(row[3])
        drivercounter=drivercounter+1
count=0
carpooldrivernum=0
track=[]
trackr=[]

for t in secondcol:
        if t=='Y':
            track.append(count)
            count=count+1
        else:
            trackr.append(count)
            count=count+1

for x in firstcol:
    address=x

    URLblank="https://maps.googleapis.com/maps/api/geocode/json?address=&key=AIzaSyAdXCiGhcQeNXQJG6cq9utetQFAo8wJl5A"
    URL=URLblank[:58] + address + URLblank[58:]

    import urllib
    googleResponse = urllib.urlopen(URL)
    jsonResponse = json.loads(googleResponse.read())
    test = json.dumps([s['geometry']['location'] for s in jsonResponse['results']], indent=3)
    splits=test.splitlines()
    splitted=[]
    #print splits
    #print 1
    splitted.append(splits[2])
    splitted.append(splits[3])

    lat=[]
    lon=[]
    for i in splitted[0]:
        if i=='.':
            lat.append(i)
        if i.isdigit():
            lat.append(i)
        if i=='-':
            lat.append(i)
    for o in splitted[1]:
        if o=='.':
            lon.append(o)
        if o.isdigit():
            lon.append(o)
        if o=='-':
            lon.append(o)
    
    latstring=''.join(lat)
    listoflat.append(latstring)
    lonstring=''.join(lon)
    listoflon.append(lonstring)
    

URLblank2="https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=&destinations=&key=AIzaSyAdXCiGhcQeNXQJG6cq9utetQFAo8wJl5A"
listoforiginlat=[]
listoforiginlon=[]

for h in track:
    originlat=listoflat[h]
    listoforiginlat.append(originlat)
    originlon=listoflon[h]
    listoforiginlon.append(originlon)
originamount=len(listoforiginlat)
destinationstring=[]
for u in range(0,len(trackr)):
    destinationstring.append(listoflat[trackr[u]])
    destinationstring.append(',')
    destinationstring.append(listoflon[trackr[u]])
    destinationstring.append('|')
destinationstring=''.join(destinationstring)
for x in range(0,originamount):
    carpooldrivernum=carpooldrivernum+1
    f = open("carpools.txt", "a")
    f.write("Carpool driver %d: %s\n" % (carpooldrivernum, drivername[carpooldrivernum-1]))
    
    URL2=URLblank2[:80] + listoforiginlat[x] + ',' + listoforiginlon[x] + URLblank2[80:]
    
    URL3=URL2[:117] + destinationstring + URL2[117:]
    
    googleResponse2 = urllib.urlopen(URL3)
    jsonResponse2 = json.loads(googleResponse2.read())
    if x == 0: 
        for column in jsonResponse2['destination_addresses']:
            pickups.append(str(column))
        for column in jsonResponse2['rows'][0]['elements']:
            distances.append(column['duration']['text'])
        for i in distances:
            b=int(re.search(r'\d+', i).group())
            time.append(b)
            
   # print pickups
    
    minutes=[]
    riders=[]
    argument=0
    #print "terminate?"
    #print driveramount
    #print argument
    argument=int(driveramount[carpooldrivernum-1])
    for d in range(0,argument):
        if len(pickups)==0:
            break
       # print "terminate2?"
        minpos=pickups.index(min(pickups))
        riders.append(pickups[minpos])
        pickups.pop(minpos)
        time.pop(minpos)
    for rider in riders:
        #if len(pickups)==0:
         #   break
        f = open("carpools.txt", "a")
        f.write("%s\n" % rider)
    f.write("\n")
f.close() 





