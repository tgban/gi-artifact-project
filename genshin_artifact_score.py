# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 00:16:28 2023

@author: canh_
"""

import genshin_artifact as ga

def danhgiatdv(mainType, mainStat, artifactLines, setName):
    # __score_v1(mainType, mainStat, artifactLines, setName)
    return __score_v2(mainType, mainStat, artifactLines, setName)

def __score_v1(mainType, mainStat, artifactLines, setName):
    if mainStat is not None and mainStat < 0:
        return None
    if len(artifactLines) <= 0:
        return None
    score = 0
    setStats = ga.setName[setName]
    allStats = {x: 0 for x in range(len(ga.stats))}
    allStats[mainStat] += 1 if mainType > 1 else 0
    for line in artifactLines:
        allStats[line] += 1
    if len(setStats) > 0:
        for stat in setStats:
            if stat < 0:
                stat += len(ga.stats)
            if stat == mainStat:
                score += 4
            if stat in artifactLines:
                numStatInSubstat = len([x for x in artifactLines if x == stat])
                score += 3 * numStatInSubstat
    # HP, Def, Atk cancels each other
    trioTypes = [i for i in range(0, 3)]
    trioTypes.sort(key = lambda a: allStats[a], reverse = True)
    for i in range(len(trioTypes)):
        if i == 0:
            score += 2 * allStats[trioTypes[i]]
            score += 2 if mainStat == trioTypes[i] else 0
        else:
            score -= 1 * i * allStats[trioTypes[i]]
    # Def, EM cancels each other. Otherwise, EM is good
    if allStats[2] > 0 and allStats[3] > 0:
        score -= 2 * (allStats[2] + allStats[3])
    else:
        score += allStats[3]
    
    # Crit lines are good
    score += 3 * (allStats[4] + allStats[5])
    
    # ER is good
    score += allStats[6]
    
    if mainStat >= 3:
        score += 1
    if mainType == 3 and mainStat >= 8:
        score += 2
    # print('Score (v1):', score)
    return score

def __score_v2(mainType, mainStat, artifactLines, setName):
    if mainStat is not None and mainStat < 0:
        return None
    if len(artifactLines) <= 0:
        return None
    attackScore = 0
    suppScore = 0
    defenseScore = 0
    setStats = ga.setName[setName]
    allStats = {x: 0 for x in range(len(ga.stats))}
    allStats[mainStat] += 1 if mainType > 1 or mainStat in range(0, 3) else 0
    for line in artifactLines:
        allStats[line] += 1
    if len(setStats) > 0:
        for stat in setStats:
            if stat < 0:
                stat += len(ga.stats)
            if stat == mainStat:
                attackScore += 4
                suppScore += 4
                defenseScore += 4
            if stat in artifactLines:
                numStatInSubstat = len([x for x in artifactLines if x == stat])
                attackScore += 3 * numStatInSubstat
                suppScore += 3 * numStatInSubstat
                defenseScore += 3 * numStatInSubstat
    # Crit
    if mainStat == 4 or mainStat == 5:
        attackScore += 5 * (allStats[4] + allStats[5])
        suppScore += 0 * (allStats[4] + allStats[5])
        defenseScore += 5 * (allStats[4] + allStats[5])
    elif allStats[4] > 0 or allStats[5] > 0:
        attackScore += 4 * (allStats[4] + allStats[5])
        suppScore += 0 * (allStats[4] + allStats[5])
        defenseScore += 4 * (allStats[4] + allStats[5])
    # HQN + TTNT
    if any([allStats[3] > 0 and allStats[6] > 0, (allStats[3] > 0 or allStats[6] > 0) and (mainStat == 3 or mainStat == 6)]):
        suppScore += 6
    elif any([allStats[3] > 0, allStats[6] > 0, mainStat == 3, mainStat == 6]):
        attackScore += 4
        suppScore += 4
        defenseScore += 0 if allStats[3] > 0 or mainStat == 3 else 2
    # Healing bonus
    if mainStat == 7:
        suppScore += 4
    # STNT
    if mainStat >= 8:
        attackScore += 6
    if mainStat == 15:
        defenseScore += 0 if allStats[3] > 0 else 6
    # Stat chính
    trioTypes = [i for i in range(0, 3)]
    trioTypes.sort(key = lambda a: allStats[a], reverse = True)
    # Thêm điểm nếu stat chính nhiều nhất (dòng chính - hoa/lông)
    if mainType > 1 and mainStat in range(0, 3):
        if mainStat == 2:
            defenseScore += 2
        else:
            attackScore += 2
            suppScore += 2
    # Thêm điểm nếu stat chính nhiều nhất (dòng phụ)
    if allStats[trioTypes[0]] > 1:
        if trioTypes[0] != mainStat and mainType > 1:
            if trioTypes[0] == 2:
                defenseScore -= 4
            else:
                attackScore -= 4
                suppScore -= 4
        elif any([allStats[trioTypes[1]] > 0 and allStats[trioTypes[2]] > 0, allStats[trioTypes[1]] > 1, allStats[trioTypes[2]] > 1]):
            # Nhiều hơn 1 stat, trừ điểm
            if trioTypes[0] == 2:
                defenseScore -= 2
            else:
                attackScore -= 2
                suppScore -= 2
        elif allStats[trioTypes[1]] > 0:
            # Nhiều hơn 1 stat (nhưng số dòng ít hơn), trừ ít điểm
            if trioTypes[0] == 2:
                defenseScore -= 1
            else:
                attackScore -= 1
                suppScore -= 1
        else:
            # Chỉ có stat chính & == main stat
            if trioTypes[0] == 2:
                defenseScore += 2
            else:
                attackScore += 2
                suppScore += 2
    else:
        if allStats[trioTypes[1]] > 0 and allStats[trioTypes[2]] > 0:
            # Nhiều hơn 1 stat, trừ điểm
            if trioTypes[0] == 2:
                defenseScore -= 4
            else:
                attackScore -= 4
                suppScore -= 4
        elif allStats[trioTypes[1]] > 0:
            # Nhiều hơn 1 stat (nhưng số dòng ít hơn), trừ ít điểm
            if trioTypes[0] == 2:
                defenseScore -= 2
            else:
                attackScore -= 2
                suppScore -= 2
    score = max(attackScore, suppScore, defenseScore)
    print('Score (v2):', str(score) + '.', 'A:', str(attackScore) + ';S:', str(suppScore) + ';D:', defenseScore)
    return score
# danhgiatdv(0, [1, 1, 3, 6], 'dấu ấn ngăn cách')