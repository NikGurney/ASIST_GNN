# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:51:15 2021

@author: gurney
"""

import os
import json
import itertools as its
import dgl
import torch as th


os.chdir('c:/Users/gurney/Documents/ASIST/teamGNN')
#extract parent room and child areas from JSON file
map_file = 'Saturn_Feb4_sm_v1.0.json'
orig_map = json.load(open(map_file,'r'))

#extracting portal names and storing them to use in edge creation
#indices from this list become the portal IDs in the graph
portal_node_names = []
for n in orig_map['connections']:
    if n['bounds']['type'] == 'rectangle':
        portal_node_names.append(n['id'])

#ditto        
room_node_names = []
for m in orig_map['locations']:
    if 'child_locations' not in m:
        room_node_names.append(m['id'])

# creating edges
# room edges contains edges going each direction
# portal edges are split into two directions for DGL
# bidirectional edges can also be done in DGL, but is explicit here for clarity
# aget edges go to every physical node and vice-versa
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

#At some point these will come in as alpha, bravo, gamma or something
#might be worthwhile connecting their names and number IDs?        
agents = 3
agent_room_edges = []
room_agent_edges = []
agent_portal_edges = []
portal_agent_edges = []
agent_agent_edges = list(its.permutations(range(agents), 2))
for i in range(agents):
    for j in enumerate(room_node_names):
        agent_room_edges.append((i, j[0]))
        room_agent_edges.append([j[0], i])
    for j in enumerate(portal_node_names):
        agent_portal_edges.append((i, j[0]))
        portal_agent_edges.append([j[0], i])        

# making the graph
g = dgl.heterograph({
        ('room', 'extends', 'room'): room_edges,
        ('room', 'into', 'portal'): room_portal_edges,
        ('portal', 'into', 'room'): portal_room_edges,
        ('agent', 'relates', 'room'): agent_room_edges,
        ('room', 'relates', 'agent'): room_agent_edges,
        ('agent', 'relates', 'portal'): agent_portal_edges,
        ('portal', 'relates', 'agent'): portal_agent_edges,
        ('agent', 'relates', 'agent'): agent_agent_edges
    })

#creating spaces to hold feature data
#10 is an arbitrary n of victims
#idx0 = triaged, float 0 to 1 as % triaged
#idx1 = critical, 1 if true
g.nodes['room'].data['victims'] = th.zeros(243, 10, 2) 
g.nodes['portal'].data['victims'] = th.zeros(93, 5, 2) 

#need to automate the n of rubble can likely get this from the csv that has locals
#float to 1 to 0 as % uncleared
g.nodes['room'].data['rubble'] = th.zeros(243, 10, 1)
g.nodes['portal'].data['rubble'] = th.zeros(243, 10, 1)

#one hot for tool 0 - med, 1 - rubble, 2 - transport
g.nodes['agent'].data['tool'] = th.zeros(3, 3, 1)
#probs of having each map
g.nodes['agent'].data['map'] = th.full((3, 3), 1/3)
#dist from center of room 1 = furthest possible
g.nodes['agent'].data['dist'] = th.zeros(3, 1)
#direction face is pointing
g.nodes['agent'].data['yaw'] = th.zeros(3, 1)
#converted from durability range 1 being max
g.nodes['agent'].data['toolLife'] = th.ones(3, 1)
#boolean for if player is swinging
g.nodes['agent'].data['swinging'] = th.zeros(3, 1)
