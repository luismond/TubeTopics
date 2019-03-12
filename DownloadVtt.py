# -*- coding: utf-8 -*-
import youtube_dl

def download_vtt(url,lang):  
    ydl_opts = {
            'quiet': True,
            'subtitleslangs': [lang],
            'writeautomaticsub': 'yes',
            'skip_download': 'yes'            
            }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])