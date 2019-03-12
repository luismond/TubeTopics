# -*- coding: utf-8 -*-
from NLP_GLOBAL import get_csv_lines
import time


def time_stamp(url, name,vid_id):
    
    timecode_lines = get_csv_lines(name+'_terms.csv')
    timecode_lines = [l for l in timecode_lines if not l==[]]
    timecode_lines = [l for l in timecode_lines if l[1]!='']
    
    def convert_HMS(seconds):
        HMS = time.strftime('%H:%M:%S', time.gmtime(seconds))
        return HMS
    
    vid_id = '123'#drop
    link_ = '<a href="https://www.youtube.com/watch?v=%vid_id&t=%secss">%hms</a>' #62s
    link_ = link_.replace('%vid_id',vid_id)
    
    lines = [[l[0].split(),l[1].split(',')] for l in timecode_lines]
    
    def combine(list1,list2):
        combined_list = []
        for i in list1:
            for j in list2:
                combined_list.append((i,j))
        return combined_list
    
    lines = [combine(l[0],l[1]) for l in lines]
    lines = [i for j in lines for i in j]
    lines = dict(lines)
    
    from collections import defaultdict
    v = defaultdict(list)
    for key, value in sorted(lines.items()):
        v[value].append(key)
    
    timecode_lines = list(v.items())
    
    times = [b for (a,b) in timecode_lines]
    
    lines = [a for (a,b) in timecode_lines]
    
    times = [[[convert_HMS(int(y)),link_.replace('%secs',y)] for y in x] for x in times]
    
    times = [[[y[1].replace('%hms',y[0])] for y in x] for x in times]
    
    times = [' '.join([' '.join(y) for y in x]) for x in times]
    
    timecode_lines = sorted(list(zip(lines,times)))
    
    
    tl12 = []
    
    for l in timecode_lines:
        span = '<span>%topic</span> <span>%timestamps</span><br>'
        new_l = span.replace('%timestamps',l[1])
        new_l = new_l.replace('%topic',l[0])
        tl12.append(new_l)
    
    #WRITE OUT HTML FILE
    with open(name+'_time_stamped_terms.html', 'w', encoding='utf8') as f:
    
        for line in tl12:
            print(line)
            f.write(line)
