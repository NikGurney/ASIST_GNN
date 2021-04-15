# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 13:12:16 2021

@author: gurney
"""

import csv
 
roomFile = 'C:/Users/gurney/Documents/ASIST/teamGNN/ASIST_GNN/saturn_rooms.csv'
portalFile = 'C:/Users/gurney/Documents/ASIST/teamGNN/ASIST_GNN/saturn_doors.csv'

with open(roomFile, 'r') as data:
    rooms = csv.DictReader(data)  
    roomList = list(rooms)

with open(portalFile, 'r') as data:
    portals = csv.DictReader(data)  
    portalList = list(portals)

x = -2216
z = -9.5

for room in roomList:
    if x >= int(room['x0']) and x < int(room['x1']) and z >= int(room['z0']) and z < int(room['z1']):
        print(room['RoomID'])