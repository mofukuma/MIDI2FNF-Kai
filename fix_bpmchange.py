#
# FNFJSONにBPMを曲の途中で変える場合の補正を行う
#

import sys
import json
from easygui import *
import os
import math
import sys

#ファイルオープンーーーーーーーーーーーーーー
# for Drag&Drop or FileDialog
path = ""
if len(sys.argv) > 1:
    path = sys.argv[1]

if path == "":
    path = fileopenbox()

bname = os.path.basename(path)
fileext = os.path.splitext(bname)[1]
filename = os.path.splitext(bname)[0]
songName = filename

print("processing: ", fileext)

if ".json" == fileext:
    # JSONファイルの読み込みと辞書への変換
    with open(path, "r") as file:
        rdat = json.load(file)
        dat = rdat["song"]

    notes = dat["notes"]
    bpm = notes[0]["bpm"]
    if "bpm" in dat:
        bpm = dat["bpm"]
    print("bpm:", bpm)
    
    ms_per_beat = 60 / bpm * 1000 
    ms_per_section =  (60*4)/bpm* 1000

    msg = f"Setting to change BPM on middle song section. Start BPM={bpm}"
    title = "FNF BPM Event Tool"
    fieldNames = ["1) Section No.", "1) BPM", "2) Section No.", "2) BPM"]
    fieldValues = [-1, -1, -1, -1] 
    fieldValues = multenterbox(msg, title, fieldNames, fieldValues)
    print(fieldValues)
    bpmevent = [[fieldValues[0], fieldValues[1]], [fieldValues[2],fieldValues[3]]]
    currTime=0

    last_bpmchangems = 0
    now_bpm = bpm
    for i in range(len(notes)):
        section = notes[i]
        for e in bpmevent:
            if int(e[0]) == i:
                last_bpmchangems = currTime
                now_bpm = float(e[1])
                print(f"bpm -> {now_bpm}")
        
        rdat["song"]["notes"][i]["bpm"] = now_bpm

        for j in range(len(section["sectionNotes"])):
            sn = section["sectionNotes"][j]
            note_time = sn[0]

            if bpm != now_bpm:
                fixtime = (note_time - last_bpmchangems) / (now_bpm / bpm)
                rdat["song"]["notes"][i]["sectionNotes"][j][0] = last_bpmchangems + fixtime

        currTime += ms_per_section
    
    out = filesavebox(default=filename+'.json')
    with open(out,"w") as f:     
        json.dump(rdat, f)
    

