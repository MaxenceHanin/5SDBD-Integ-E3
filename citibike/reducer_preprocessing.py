#!/usr/bin/python
import sys

print("id_o,id_d,duration,distance,hour,weekday,month,type,gender,age,lat_o,long_o,lat_d,long_d")
for line in sys.stdin:
        l = line.split(',')
        # Filter only subscribers and people aged between 18 and 80
        if (int(l[7]) == 1 and int(l[9])>=18 and int(l[9])<=80):
                print(line.strip())
