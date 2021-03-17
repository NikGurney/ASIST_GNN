# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:51:15 2021

@author: gurney
"""

import os
import json
import itertools as its
import dgl


os.chdir('c:/Users/gurney/Documents/ASIST/teamGNN')
#extract parent room and child areas from JSON file
map_file = 'Saturn_Feb4_sm_v1.0.json'
orig_map = json.load(open(map_file,'r'))

portal_node_names = []
for n in orig_map['connections']:
    if n['bounds']['type'] == 'rectangle':
        portal_node_names.append(n['id'])
        
room_node_names = []
for m in orig_map['locations']:
    if 'child_locations' not in m:
        room_node_names.append(m['id'])

room_edges = []
portal_room_edges = []
room_portal_edges = []
for i in orig_map['connections']:
    if 'extension' in i['type']:
        room_indices = []
        for k in i['connected_locations']:
            room_indices.append(room_node_names.index(k))    
        room_edges.extend(list(its.permutations(room_indices, 2)))
        del room_indices
    else:
        room_indices = []
        for k in i['connected_locations']:
            room_indices.append(room_node_names.index(k))
        portal_index = portal_node_names.index(i['id'])
        portal_room_edges.extend(its.product([portal_index], room_indices))
        room_portal_edges.extend(its.product(room_indices, [portal_index]))
        del room_indices
        del portal_index

g = dgl.heterograph({
        ('room', 'extends', 'room'): room_edges,
        ('room', 'into', 'portal'): room_portal_edges,
        ('portal', 'into', 'room'): portal_room_edges
    })

