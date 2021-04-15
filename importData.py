# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 08:41:03 2021

@author: gurney
"""

import os
import json

os.chdir('C:\\Users\\gurney\\study-2_pilot-2_2021.02\\gnnPilotData')
#extract parent room and child areas from JSON file

tempDic = {}
tempRow = {}
d = {}
n = 0
ignoreCases = ['ASIST3', 'Mission Timer not initialized.', 'Status:UserSpeech',
               'Event:PlayerJumped', 'Mission:VictimList', 'Mission:BlockageList',
               'SemanticMap:Initialized', 'experiment_author', '"mission_state":"Start"',
               '"mission_state":"Stop"']
for file in os.listdir():
    if file.endswith(".metadata"):
        with open(file) as fp:
            for cnt, row in enumerate(fp):
                if any(x in row for x in ignoreCases):
                    continue
                tempRow = json.loads(row)
                tempDic[cnt] = tempRow['data']
                tempRow = {}
            d[n] = tempDic   
            n += 1
            tempDic = {}

aaa = {}
fileName = 'NotHSRData_TrialMessages_CondBtwn-TmPlan_CondWin-SaturnB_Trial-T000291_Team-TM000009_Member-P000127-P000128-P000129_Vers-2.metadata'

with open(fileName) as fp:
    for cnt, row in enumerate(fp):
        aaa[cnt] = json.loads(row)