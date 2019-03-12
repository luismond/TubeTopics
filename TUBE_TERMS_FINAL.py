# -*- coding: utf-8 -*-
from DownloadVtt import download_vtt
from VttToCsv import vtt_to_csv
from GetTerms2 import get_terms
from TimeStampTerms3 import time_stamp
from PostTermsWP import post_terms
import glob, os

'''
import youtube_dl
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet':True,})
yt_url = "https://www.youtube.com/user/GRadioCentro/videos"

with ydl:
    result = ydl.extract_info(yt_url, download=False) 
    urls = [item['webpage_url'] for item in result['entries']]

#for url in urls:
'''

url = 'https://www.youtube.com/watch?v=HbxPW3VMFos'

download_vtt(url,'es') 
name =  max(glob.iglob('*.vtt'), key=os.path.getctime)[:-4]  
vid_id = url[-11:]
vtt_to_csv(name)        
get_terms(name)    
time_stamp(url,name,vid_id)
#post_terms(url,name)
    

        
