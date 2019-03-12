import csv, re, os
from SetOrdered import OrderedSet
from NLP_GLOBAL import drop_substrings

#name = 'La historia de los ángeles _ DW Documental-4F_YSo40wKU.es'
def vtt_to_csv(name): 
    with open(name+'.vtt', 'r', encoding='utf8') as file:
        text = file.read()
    
    #SPLIT ON DOUBLE NEWLINE, IMPORTANT
    segments = text.split('\n\n') 
    
    #CLEAN SEGMENTS
    reg1 = re.compile(r"\<.*?\>")#Strips unwanted tags
    reg2 = re.compile(r"\.+\d+")#Strips the miliseconds
    
    def clean(content):    
        new_content = reg1.sub('',content)
        new_content = reg2.sub('',new_content)
        new_content = new_content.replace('align:start position:0%','')
        new_content = new_content.replace('-->','')
        new_content = new_content.replace(u'[Música]','')
        new_content = new_content.replace(u'[Aplausos]','')
        new_content = new_content.replace(u'[Risas]','')
        new_content = new_content.replace(u'[Laughter]','')
        new_content = new_content.replace(u'[Music]','')
        new_content = new_content.replace(u'[Applause]','')
        return new_content
    
    clean_segments = [clean(s) for s in segments if len(s)!=0][2:]
    
    trimmed_segments = []
    for segment in clean_segments:
        split_segment = segment.split()
        time_code = split_segment[0] 
        hms = time_code.split(':')
        seconds = int(hms[0])*3600 + int(hms[1])*60 + int(hms[2])
        text = ' '.join(segment.split()[2:])
        trimmed_segment = (seconds, text) 
        trimmed_segments.append(trimmed_segment)
    ts_lines = trimmed_segments
    
    ########### CONDENSE ########################
    lines = [''.join(l[1]) for l in ts_lines]
    lines = list(OrderedSet(lines))
    avg_len = sum(len(l) for l in lines)/len(lines)
    lines_short = [l for l in lines if len(l) < avg_len and len(l)>2]
    drop_substrings(lines_short)
    lines_long = [l for l in lines if len(l)> avg_len]
    
    #CHECK for the long ones, if they are NOT in the joined shorts. 
    lines_long_absent = [l for l in lines_long if not l in ' '.join(lines_short)]
    
    #If they are not there, and they start like a short, I replace the short with the long.
    for line in lines_short:
        for line_ in lines_long_absent:
            if line_.startswith(line):
                #print(line_)
                lines_short[lines_short.index(line)] = line_
    
    ts_condensed_lines = []
    for l in ts_lines:
        if l[1] in lines_short:
            ts_condensed_lines.append(l)
    
    #MORE CONDENSING. CONVERT TO DICT TO ELIMINATE VALUE DUPLICATES  
    ts_times = [l[0] for l in ts_condensed_lines]
    ts_lines = [l[1] for l in ts_condensed_lines]
    #ts_x = list(zip(ts_times,ts_lines))
    ts2 = dict(zip(ts_lines, ts_times))
    ts3 = []
    for k,v in ts2.items():
        temp = [k,v]
        ts3.append(temp)
    ts4 = list(sorted([[int(b),a] for (a,b) in ts3]))
    
    #JOIN TWO CONSECUTIVE LINES, KEEP JUST ONE TIMESTAMP
    ts5 = [[l,l_[1]] for (l,l_) in zip(ts4[0::2],ts4[1:][0::2])]
    ts6 = [[str(l[0][0]),l[0][1],l[1]] for l in ts5]
    ts7 = [[l[0],[l[1],l[2]]] for l in ts6]
    ts8 = [[l[0],' '.join(l[1])] for l in ts7]  
    
    #ts8 = [','.join(t) for t in ts8]
    

    #WRITE OUT CSV FILE
    with open(name+'.csv', 'w', encoding='utf8',newline='') as f:
        thewriter = csv.writer(f)
        for line in ts8:
            thewriter.writerow(line)
