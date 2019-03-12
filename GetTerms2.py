# -*- coding: utf-8 -*-
from nltk import FreqDist
from nltk.util import ngrams
from SpanishStopWords import stops_es as stops
from NLP_GLOBAL import get_csv_lines, strip_punct, drop_substrings, remove_stops
import csv
import time
import stanfordnlp
from gensim import corpora, models
import pandas as pd
MODELS_DIR = 'C:\\Users\\agent\\stanfordnlp_resources\\'
nlp = stanfordnlp.Pipeline(processors='tokenize,pos', models_dir=MODELS_DIR, lang='es')

start = time.time()

def join_two_consec_time_stamped_lines(ts_lines):
    ts_lines = [[l,l_[1]] for (l,l_) in zip(ts_lines[0::2],ts_lines[1:][0::2])]
    ts_lines = [[str(l[0][0]),l[0][1],l[1]] for l in ts_lines]
    ts_lines = [[l[0],[l[1],l[2]]] for l in ts_lines]
    ts_lines = [[l[0],' '.join(l[1])] for l in ts_lines]
    return ts_lines



def get_terms(name):
    
    #GET TOP TFIDF LINES
    
    csv_file = get_csv_lines(name+'.csv')
    csv_file = join_two_consec_time_stamped_lines(csv_file)
    csv_file = join_two_consec_time_stamped_lines(csv_file)
    
    lines = pd.DataFrame(csv_file)
    lines.columns = ['times','lines']
    
    #lines['lines_ns'] = lines['lines'].apply(lambda x: remove_stops(x))
    #lines['lines_ns'] = lines['lines_ns'].str.split()
    lines['lines_ns'] = lines['lines'].str.split()
    dict_ = corpora.Dictionary(lines['lines_ns'])
    #BOW
    lines['bow'] = lines['lines_ns'].apply(lambda x: dict_.doc2bow(x))
    #TFIDF
    tfidf = models.TfidfModel(lines['bow']) 
    lines['tfidf'] = lines['bow'].apply(lambda x: tfidf[x]) 
    def tfidf_sum(x):
        return sum([b for a,b in x])
    lines['tfidf_sum'] = lines['tfidf'].apply(lambda x: tfidf_sum(x))
    lines['len'] = lines['lines_ns'].str.len()
    lines['avg'] = lines['tfidf_sum']/lines['len']
    
    def get_top(lines):
        ns = list(set([n for n in lines['len'].tolist()]))
        sub_dfs = [lines[lines['len']==n] for n in ns]
        new_sub_dfs = []
        for sub in sub_dfs:
            sub = sub.sort_values(by=['avg'], ascending=False)
            top = round(.7 * len(sub))
            sub = sub.iloc[:top]
            new_sub_dfs.append(sub)
        return pd.concat(new_sub_dfs)
    
    lines = get_top(lines)
    lines['times'] = lines['times'].astype(int)
    lines = lines.sort_values(by=['times'], ascending=True)
    lines = list(zip(lines['times'].tolist(), lines['lines'].tolist()))
    
    #################################################

   
    times = [l[0] for l in lines]
    lines = [l[1] for l in lines]
    lines = [strip_punct(l) for l in lines]
    print (time.time()-start)
    lines = [l.split() for l in lines]
    
    
     
    
    def get_grams(lines,n):   
        lines = [list(ngrams(l,n)) for l in lines]
        lines = [[' '.join(list(x)) for x in y] for y in lines]
        lines = [[g for g in l 
                  if not g.split()[0] in stops 
                  and not g.split()[0].endswith('mente')
                  and not g.split()[-1].endswith('mente')
                  and not g.split()[-1] in stops] for l in lines]    
        
        lines = [l for l in lines if len(l)>0]
        lines_fd = FreqDist([g for l in lines for g in l])
        once_grams = [g[0] for g in list(lines_fd.items()) if g[1]==1]
        top_grams = list(lines_fd.most_common(200))
        top_grams = [a for (a,*b) in top_grams]
        lines = [[g for g in l if not g in once_grams and g in top_grams] for l in lines]
        lines = [list(set(l)) for l in lines]
        
        ###########
        #POS
        all_grams = list(set([g for l in lines for g in l]))
        docs = [nlp(g) for g in all_grams]
        tagged_sents_w = [[[w.text for w in sent.words] for sent in doc.sentences] 
                        for doc in docs]
        tagged_sents_t = [[[w.pos for w in sent.words] for sent in doc.sentences] 
                        for doc in docs]
        tagged_sents_ = list(zip(tagged_sents_w,tagged_sents_t))
        print(tagged_sents_)
        tagged_sents = [(' '.join(w[0]),' '.join(t[0])) for w,t in tagged_sents_]
        tagged_sents = [w for w,t in tagged_sents if 'VERB' in t or 'ADV' in t]
        lines = [[g for g in l if not g in tagged_sents] for l in lines]
        #############
        print (time.time()-start)    
        return lines
        
    lines1 = get_grams(lines,1) 
    lines2 = get_grams(lines,2) 
    lines3 = get_grams(lines,3)
    
    linesg = list(zip(lines1,lines2,lines3))
    linesg = [[','.join(g) for g in l if not g==[]] for l in linesg]
    linesg = [','.join(l) for l in linesg]
    linesg = [l.split(',') for l in linesg]
    
    linesg = [drop_substrings(l) for l in linesg]
    linesg = [drop_substrings(l) for l in linesg]
    linesg = [drop_substrings(l) for l in linesg]
    linesg = [sorted(l) for l in linesg]
    
    linesg = [','.join(l) for l in linesg]
    print(linesg)
    linesg_t = list(zip(times,linesg))
    linesg_t = [(a,b) for (a,b) in linesg_t if not b=='']
    
    linesg = ','.join(linesg).split(',')
    linesg = list(set(linesg))
    linesg = [l for l in linesg if not l=='']
    
    #WRITE OUT CSV FILE
    with open(name+'_terms.csv', 'w', encoding='utf8') as f:
        thewriter = csv.writer(f)
        for line in linesg_t:
            thewriter.writerow(line)
    with open(name+'_terms.txt', 'w', encoding='utf8') as f:
        for l in linesg:
            f.write(l+'\n')

    print (time.time()-start)