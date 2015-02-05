# -*- coding:utf-8 -*-
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

file_name = 'result.html'   #網頁檔名
html_file = open(file_name, 'r')   #開啟網頁
html = html_file.read()   #讀取檔案
html_file.close()   #關閉檔案

soup = BeautifulSoup(html)
dom_of_likes = soup.select('#collection_wrapper_2409997254')[0]   #選取likes的DOM

target_file = open('target_file.txt','w')   #建立目標檔案

likes = dom_of_likes.select('._6b')   #選取包含like名字,id,類型的class

for like in likes:    
    if like.text.encode('utf-8') != '':
        row = []   #建立空的list，之後將like的名字,id,類型丟進去
        name_of_like = like.select('.fsl a')[0].text   #like的名字
        id_of_like = like.select('.fsl a')[0]['data-gt'].replace('{"engagement":{"eng_type":"1","eng_src":"2","eng_tid":"','').replace('","eng_data":[]}}','')   #like的id   
        type_of_like = like.select('._5k4f')[0].text   #like的類型        
#        print name_of_like,id_of_like,type_of_like
        
        #將like的名字,id,類型丟進row[]
        row.append(name_of_like)
        row.append(id_of_like)
        row.append(type_of_like)

        target_file.write(','.join(row).encode('utf-8') + '\n')   #like的名字,id,類型丟進去

target_file.close()
print 'DONE'