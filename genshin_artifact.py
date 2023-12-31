# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 06:44:30 2023

@author: canh_
"""
import string_comparison as sc
import vietuniproc as vp

types = (
    'hoa sự sống',
    'lông vũ tử vong',
    'cát thời gian',
    'ly không gian',
    'nón lý trí',
)

stats = (
    'tấn công',
    'hp',
    'phòng ngự',
    'tinh thông nguyên tố',
    'tỷ lệ bạo kích',
    'st bạo kích',
    'hiệu quả nạp nguyên tố',
    'tăng trị liệu',
    'tăng sát thương vật lý',
    'tăng st nguyên tố hỏa',
    'tăng st nguyên tố thủy',
    'tăng st nguyên tố thảo',
    'tăng st nguyên tố lôi',
    'tăng st nguyên tố phong',
    'tăng st nguyên tố băng',
    'tăng st nguyên tố nham',
)

setName = {
    'dũng sĩ trong băng giá': (-2,),
    'tôn giả trầm lặng': (),
    'hiền nhân bốc lửa': (),
    'thiếu nữ đáng yêu': (7,),
    'lễ bế mạc của giác đấu sĩ': (0,),
    'bóng hình màu xanh': (-3,),
    'đoàn hát lang thang đại lục': (3,),
    'như sấm thịnh nộ': (-4,),
    'diệm liệt ma nữ cháy rực': (-7,),
    'nghi thức tông thất cổ': (6,),
    'kỵ sĩ đạo nhuốm máu': (-8,),
    'phiến đá lâu đời': (-1,),
    'sao băng bay ngược': (1,),
    'trái tim trầm luân': (-6,),
    'thiên nham vững chắc': (1,),
    'lửa trắng xám': (-8,),
    'dòng hồi ức bất tận': (0,),
    'dấu ấn ngăn cách': (6,),
    'giấc mộng phù hoa': (2,),
    'xà cừ đại dương': (7,),
    'thần sa vãng sinh lục': (0,),
    'dư âm tế lễ': (0,),
    'ký ức rừng sâu': (-5,),
    'giấc mộng hoàng kim': (2,),
    'sử ký đình đài cát': (-3,),
    'đoá hoa trang viên thất lạc': (3,),
    'giấc mộng thuỷ tiên': (-6,),
    'vầng sáng vourukasha': (1,),
    'đoàn kịch hoàng kim': (),
    'thợ săn marechaussee': (),
}

stringMatchPercent = 0.8
maxAllowedDiff = 2

def find_text_in_list(text, texts):
    maxMatch = float('inf')
    minDist = float('inf')
    minChar = float('inf')
    name = -1
    # dist = zip(texts, [sc.levenshtein_dist(text, texts) for t in texts])
    # dist = [(t, d) for t, d in dist if d < (1 - stringMatchPercent) * len(t) or vp.khongdau(t) in vp.khongdau(text)]
    # for setLine in setName.keys():
    #     match = 1 - sc.percent_string_diff(text, setLine)
    #     if match > stringMatchPercent and match > maxMatch:
    #         name = setLine
    #         maxMatch = match
    # return name if name else None
    # print(text)
    for i in range(len(texts)):
        dist = sc.levenshtein_dist(text, texts[i])
        lenDiff = abs(len(text) - len(texts[i]))
        charDiff = abs(dist - lenDiff)
        diff = lenDiff * charDiff
        # print('\t', dist, lenDiff, charDiff, diff)
        inText = vp.khongdau(texts[i]) in vp.khongdau(text)
        underDist = dist < (1 - stringMatchPercent) * len(texts[i])
        lowDiff = dist < minDist and diff < maxMatch
        lowCharDiff = dist < minDist and charDiff < lenDiff
        if inText:
            name = i
            maxMatch = diff
            minDist = dist
            minChar = charDiff
            break
        elif underDist or lowDiff or lowCharDiff:
        # if maxMatch >= diff and minChar >= charDiff and diff < maxAllowedDiff ** 2 and charDiff < stringMatchPercent * len(stats[statIdx]):
            name = i
            maxMatch = diff
            minDist = dist
            # minLen = lenDiff
            minChar = charDiff
    return (None, None) if name < 0 or minChar > min(len(text), len(texts[name])) * (stringMatchPercent ** 2) else (name, maxMatch)
        
def find_type(text):
    global types
    return find_text_in_list(text, types)

def find_set(text):
    global setName
    setKeys = list(setName.keys())
    setIdx, score = find_text_in_list(text, setKeys)
    return (setKeys[setIdx] if setIdx is not None and setIdx >= 0 else None, score)

def find_stat(text):
    global stats
    return find_text_in_list(text, stats)

# print('Type:')
# print(find_type('z4.'))
# print(find_type('non ly p'))
# print(find_type(') 150)'))
# print(find_type('nón bình lôi'))
# print('Set:')
# print(find_set('h'))
# print(find_set('- hp+ 9%'))
# print('Stat:')
# print(find_stat('* hiệu quả nạp nguyên'))
# print(find_stat('la'))
# print(find_stat('- hp+ 9%'))
# print(find_stat('tăng st nguyên tó phot'))
# for i in setName.keys():
    # print(vp.khongdau(i))