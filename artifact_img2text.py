# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 05:12:00 2023

@author: canh_
"""
import pytesseract as tes
import genshin_artifact as ga
import math

UPPER_CUTOFF = 0.5
LOWER_CUTOFF = 0.5

def phathientdv(arr):
    h, w, _ = arr.shape
    cutoff = int(h * UPPER_CUTOFF)
    lowCutoff = int(h * LOWER_CUTOFF)
    mainLines = tes.image_to_string(arr[:cutoff, :int(w * 0.68)], lang='vie')
    mainLines = [i for i in mainLines.lower().split('\n') if i]
    text = tes.image_to_string(arr[lowCutoff:], lang='vie')
    lines = [i for i in text.lower().split('\n') if i]
    if len(lines) <= 0 or len(mainLines) <= 0:
        return None, None, [], None
    mainStat = -1
    mainType = -1
    # print(mainLines)
    # Find type
    minTypeScore = math.inf
    typeLine = -1
    for mainLine in range(len(mainLines)):
        artifactType, score = ga.find_type(mainLines[mainLine])
        if artifactType is not None and score < minTypeScore:
            # print('\t' + ga.types[artifactType])
            mainType = artifactType
            minTypeScore = score
            typeLine = mainLine
    if mainType < 0:
        print('Can\'t find artifact type')
        return None, None, [], None
    # Find main stat
    minMainScore = math.inf
    if len(mainLines) == 3:
        mainStat = 1
        mainIdx = len(mainLines) - 1
    else:
        minMainScore = math.inf
        for mainLine in range(typeLine, len(mainLines)):
            stat, score = ga.find_stat(mainLines[mainLine])
            if stat is not None and score < minMainScore:
                # print('\t' + ga.stats[stat])
                mainStat = stat
                minMainScore = score
    if mainStat < 0:
        print('Can\'t find main stat')
        return None, None, [], None
    # Extra check to confirm main stat for flower/feather is consistent
    if any([mainType == 0 and mainStat != 1, mainType == 1 and mainStat != 0]):
        print('Type/main stat discrepancy found. Trying to resolve...')
        if minTypeScore > minMainScore:
            print('Type change')
            mainType = 0 if mainStat == 1 else 1
        elif minTypeScore < minMainScore:
            print('Main stat change')
            mainStat = 0 if mainType == 1 else 1
        else:
            print('Can\'t reach type/main stat consistency. Currently detected type', mainType, 'with stat', mainStat)
            return None, None, [], None
    # Find set
    setName = ''
    line = -1
    # print(lines)
    minScore = math.inf
    for lineIdx in range(len(lines) - 1, -1, -1):
        s, score = ga.find_set(lines[lineIdx])
        if s and score < minScore:
            # print('\tset name', setName, 'on line', lineIdx)
            setName = s
            line = lineIdx
            minScore = score
    if not setName:
        print('Can\'t find set name')
        return None, None, [], None
    # Find stats
    stats = []
    for lineIdx in range(line - 1, -1, -1):
        if len(stats) >= 4:
            break
        stat, _ = ga.find_stat(lines[lineIdx])
        if stat is not None:
            # print('\t\t' + ga.stats[stat])
            stats.append(stat)
    validRange = len(stats) in range(3, 5)
    max1ElementMainLine = len([x for x in stats if x >= 8]) < 1
    if validRange and max1ElementMainLine:
        # print(setName, 'from\n\t', lines[line])
        # print(ga.stats[mainStat], 'from\n\t', mainLines)
        # print([ga.stats[x] for x in stats], 'from\n\t', lines[:line])
        return mainType, mainStat, stats, setName
    print('Can\'t find substats')
    return None, None, [], None
