#!/usr/bin/env python

#from https://rosettacode.org/wiki/Haversine_formula#Python
import csv
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, asin

def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8  # Earth radius in kilometers

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))

    return R * c


with open('../datasets/201801-citibike-tripdata.csv','r') as _in:
    reader = csv.reader(_in)
    print(reader.__next__())
    with open('../datasets/201801-clean.csv','w',newline='') as _out:
        writer = csv.writer(_out)
        for line in reader:
            id_o, id_d = line[3], line[7]
            dur = int(line[0])
            # dur = timedelta(seconds=int(line[0]))
            ((lat_o,long_o),(lat_d,long_d)) = ((float(line[5]),float(line[6])),(float(line[9]),float(line[10])))
            dis = haversine(lat_o,long_o,lat_d,long_d)
            st = datetime.strptime(line[1],'%Y-%m-%d %H:%M:%S.%f')
            h = st.hour
            m = st.month
            w = st.weekday()
            if line[12] == "Subscriber":
                typ = 1
                gen = 1 if int(line[14])==1 else -1
                age = st.year - int(line[13])
            else:
                typ = -1
                gen = 0
                age = 0
            #print(id_o, id_d, dur, dis, h, w, m, typ, gen, age, lat_o, long_o, lat_d, long_d)
            writer.writerow([id_o, id_d, dur, dis, h, w, m, typ, gen, age, lat_o, long_o, lat_d, long_d])
