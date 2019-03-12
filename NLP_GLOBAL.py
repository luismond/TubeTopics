# -*- coding: utf-8 -*-
#from nltk import word_tokenize
from nltk import FreqDist
from nltk.util import ngrams
from collections import defaultdict
from SpanishStopWords import stops_es 
import csv


#Find and drop substrings
def drop_substrings(lines):
    for line in lines:
        #x=' '.join(line.split()[:-2])
        for line_ in lines:
            if line != line_ and line in line_:
                lines.remove(line)
                break
    return lines    


def strip_punct(line):
    line = str(line)
    charset = set()
    for ch in line:
        charset.update(ch)
    punct = [ch for ch in charset if not ch.isalpha()]# and not ch.isdigit()]
    if ' ' in punct:
        punct.remove(' ')
    for ch in punct:
        line = line.replace(ch, ' ').lower()
        line = line.replace('  ', ' ').lower()
        #line = line.split()
    return line


def remove_stops(line):
    line = line.split()
    return ' '.join([w for w in line if not w in stops_es])# and not w.isdigit()])# and len(w)>2])

def get_csv_lines(file):
    with open(file, 'r', encoding='utf8') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
        return rows
                 

def get_text_lines(f):
    with open(f, 'r', encoding='utf-8') as f:
        return f.read().split('\n')

'''
def convert_1252_utf8(name):
    with open(name, 'r', encoding='Windows-1252') as f:
        lines = f.read().split('\n')
    lines = [l for l in set(lines) if not l.startswith('<')]
    lines_ = [l.split() for l in lines]
    print_(lines_)
    with open(name+'.txt', 'w', encoding='utf8') as f:
        for line in lines:
            f.write(line+'\n')    

def remove_stops(line):
    line = line.split()
    return [w for w in line if not w in stops_es and not w.isdigit() and len(w)>2] 
    #line = ' '.join(line)
            #and not w.endswith('ar') and not w.endswith('er') and not w.endswith(u'ír')
            #and not w.endswith('ir')]


def strip_punct(lines):
    lines = [' '.join(line) for line in lines]
    #lines = get_text_lines(name+'.txt')
    #print('text has  ' + str(len(text)) + ' lines')
    #lines = text
    lines = [l for l in lines if not l=='']
    charset = set()
    for line in lines:
       for ch in line:
           charset.update(ch)
    punct = [ch for ch in list(set(charset)) if not ch.isalpha() and not ch.isdigit()]
    print(punct)
    if ' ' in punct:
        punct.remove(' ')
    for char in punct:
        lines = [line.replace(char, ' ').lower() for line in lines]    
    return lines
    #with open(name+'_no_punct.txt', 'w', encoding='utf8') as f:
    #    for line in lines:
    #        f.write(line+'\n')
        
                 
def get_all_grams(list_of_tokenized_lines,n):   
        gramed_line_tokens = [ngrams(l,n) for l in list_of_tokenized_lines]
        all_grams = [list(l) for l in gramed_line_tokens]
        all_grams_ = []
        for l in all_grams:
            for b in l:
                all_grams_.append(b)      
        return all_grams_
                 
def get_charset(text):
    charset = set()
    for line in text:
        for ch in line:
            charset.update(ch)
    return charset             
                 



#ANALIZE TOKENS
def tokens(lines):
    for l in lines:
        for x in l:
            if type(x)==float:
                l.remove(x)
    tokens = [' '.join(l) for l in lines]
    tokens = ' '.join(tokens).split()
    print('Total tokens:')
    print(len(tokens))
    print('Unique tokens:')
    print(len(list(set(tokens))))
    fd = FreqDist(tokens)
    print('Top tokens:')
    print (fd.most_common(30))                 
                 



                 
def print_(x):
    n = 1
    print('Total lines:')
    print(len(x))
    print('Type lines:')
    print(type(x))
    print('Type lines[0]:')
    print(type(x[n]))
    print('Lines[0][0:20]:')
    #print(x[n][0:30])
    tokens(x)
    print('\n')
    
def get_clean_lines(lines):
    j_lines = [' '.join(l) for l in lines]
    tokens = ' '.join(j_lines).split()
    tokens = list(set(' '.join(tokens).split()))
    lengths = [len(t) for t in tokens]
    avg = sum(lengths) / len(tokens)
    #return lengths
    clean_lines = []
    for line in lines:
        line = [''.join(ch) for ch in line if not ch in punctuation]
        line = [w for w in line if len(w) < avg*3]
        if len(line)>2:
            clean_lines.append(''.join(line).lower())
    return clean_lines

def tokenize(line):
    line = line.split()
    #nltk_tokenize
    #line = [w.lower() for w in line]
    return [w for w in line if not w in stop_words_es and not w.isdigit()] 
            #and not w.endswith('ar') and not w.endswith('er') and not w.endswith(u'ír')
            #and not w.endswith('ir') and len(w)>2]


nlp = spacy.load('es', disable=['parser', 'ner'])
def lemmatize_es(lines):#, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    lines_out = []
    for line in lines:
        doc = nlp(" ".join(line)) 
        lines_out.append([token.lemma_ for token in doc])# if token.pos_ in allowed_postags])
    return lines_out

nlp = spacy.load('en', disable=['parser', 'ner'])
def lemmatize_en(lines, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    lines_out = []
    for line in lines:
        doc = nlp(" ".join(line)) 
        lines_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return lines_out

   

#remove stopwords
#stop_ids = [dictionary.token2id[stopword] for stopword in stoplist 
#            if stopword in dictionary.token2id]

def get_vocabulary(lines):
    vocabulary = set()
    for line in lines:
        words = tokenize(line)
        vocabulary.update(words)
    vocabulary = list(vocabulary)
    return vocabulary

def remove_unique_words(lines):
    frequency = defaultdict(int)
    for line in lines:
        for token in line:
            frequency[token] += 1
    lines = [[token for token in line if frequency[token] > 1] for line in lines]
    return lines

#memory friendly for bigger corpora:
#Create class to convert lines to bow vectors. 
class MyCorpus(object):
    def __iter__(self):
        for line in lines:
            yield dictionary.doc2bow(line)
corpus = MyCorpus()

with open('Angola.csv', 'r', encoding='utf8') as tempfile:
    lines = csv.reader(tempfile)
    lines = [l[1] for l in lines if l[1]!='']
lines = [tokenize(d) for d in lines]
lines = remove_unique_words(lines)
lines = [l for l in lines if not l==[]]

import codecs
input_file = codecs.open("Top500Twitter.csv", "r", encoding='utf-8', errors='replace')
output_file = open("Top500Twitter.csv_clean.csv", "w", encoding='utf-8')
def sanitize_characters(input_file, output_file):    
    for line in input_file:
        output_file.write(line)
sanitize_characters(input_file, output_file)

'''