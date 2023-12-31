# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 07:10:00 2023

@author: canh_
"""
import vietuniproc as vp

def percent_string_diff(c1, c2, khongdau=True):
    base = c1 if not khongdau else vp.khongdau(c1)
    comp = c2 if not khongdau else vp.khongdau(c2)
    base = [x for x in base if x]
    comp = [x for x in comp if x]
    base.sort(key=vp.khongdau)
    comp.sort(key=vp.khongdau)
    baseidx = 0
    compidx = 0
    while baseidx < len(base) and compidx < len(comp):
        compiter = compidx
        while compiter < len(comp) and vp.khongdau(base[baseidx]) >= vp.khongdau(comp[compiter]):
            if base[baseidx] == comp[compiter]:
                base.pop(baseidx)
                comp.pop(compiter)
                baseidx -= 1
                compidx = compiter
                break
            else:
                compiter += 1
        baseidx += 1
    return (len(base) + len(comp)) / (len(c1) + len(c2))

def levenshtein_dist(c1, c2, khongdau=True):
    base = c1 if not khongdau else vp.khongdau(c1)
    comp = c2 if not khongdau else vp.khongdau(c2)
    prevdist = [x for x in range(0, len(comp) + 1)]
    currdist = [0 for x in range(0, len(comp) + 1)]
    for i in range(0, len(base)):
        currdist[0] = i + 1
        
        for j in range(0, len(comp)):
            deletionCost = prevdist[j + 1] + 1
            insertionCost = currdist[j] + 1
            substitutionCost = prevdist[j] + (0 if base[i] == comp[j] else 1)
            currdist[j + 1] = min(deletionCost, insertionCost, substitutionCost)
        temp = prevdist
        prevdist = currdist
        currdist = temp
    return prevdist[len(comp)]