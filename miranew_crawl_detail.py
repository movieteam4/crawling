# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:52:53 2024

@author: ASUS
"""

import requests as rq
sess=rq.Session()
links=['https://www.miranewcinemas.com/Movie/Index?type=NowShowing','https://www.miranewcinemas.com/Movie/Index?type=ComingSoon']
detail_result={}
for link in links:
    r=sess.get(link,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
    r=r.text.split('<script type="text/javascript">')[2].split('MovieCName')[1:-11]
    for i in r:
        i=('movie_name_tw:'+i.replace('\\','').split('。')[0][3:]).split(',')
        i[0]=i[0][14:-1].replace('(普)','').replace('(輔15級)','').replace('(輔12級)','').replace('(限)','').replace('(護)','')
        i[1]=i[1][13:].strip('"').replace('(G)','').replace('(PG-15)','').replace('(PG-12)','').replace('(R)','').replace('(P)','')
        i[2]=i[2][14:].strip('"')
        # i[3]=i[3][12:].strip('"')
        i[5]=i[5][8:].strip('"')
        i[7]=i[7][11:].strip('"')
        i[8]=' '.join(i[8][8:].strip('"').split('rn'))
        i[9]=i[9][14:].strip('"')
        detail_result[i[0]]=i[1:3]+i[5:6]+i[7:]
        
                    

    
