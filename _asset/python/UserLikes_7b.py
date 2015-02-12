# -*- coding:utf-8 -*-
import requests, sys
from bs4 import BeautifulSoup

fan_page_id = '57613404340'

#用for迴圈依序讀取csv檔 
    page = n
    file_name = 'data/fan_list_' + fan_page_id + '_' + str('%05d' %page) + '.csv' #檔名     
    fans_file = open(file_name, 'r') #開啟csv檔
    fans_info = fans_file.readlines() #逐行讀取檔案，每行為一個字串
#    print len(fans_add)

#用for迴圈抓取每行粉絲的頁面網址
    for line in range(0,len(fans_info)):
        pos_1 = fans_info[line].find(',',0) #找到第一個逗點位置
        pos_2 = fans_info[line].find(',',pos_1+1) #找到第二個逗點位置
#        print pos
        fans_add = fans_info[line][pos_2+1:] #從第二個逗點後的字串為要抓取的網址
#        print fans_add
    
        res = requests.get(fans_add)
#        print res
        if res.status_code == 200:  #判斷網頁是否打得開，Response 200  //修改
#            print 'y'
            user_id = fans_info[line][0:pos_1] #從csv檔裡取得user id
            userlikes = open('userlikes_' + user_id + '.csv','a') #建立檔名為user id的csv檔
            sys.stdout.write(user_id + ' is processing...') 
            
            html = res.text.split('<!-- ')[4].split('-->')[0] #將包含likes內容的dom的註解刪除
#            print html

            likes = BeautifulSoup(html)
            
            #user的頁面本身沒有粉絲頁的id，必須要進入粉絲頁裡抓取id。likes區塊分三部分mediaPageName、visible、hiddenItem、           
            likes_mediaPageName = likes.select('.mediaRowItem') #選取第一個部分的like        
            for page in likes_mediaPageName: 
                page_add = page['href'] #抓出粉絲頁的網址
#                print page_add
                page = requests.get(page_add) #送出粉絲頁的requests
                page_soup = BeautifulSoup(page.text)
#                print page_soup
                page_id = page_soup.select('#pagelet_timeline_main_column') #選取含有粉絲頁id的dom
#                print page_id
                for p in page_id:
                    userlikes.write(user_id + ',' + p['data-gt'].split('"')[3] + '\n') #將粉絲id及粉絲頁id寫進檔案裡
            
            likes_visible = likes.select('.visible a') #選取第二個部分的like
            for page in likes_visible:
                page_add = page['href']
#                print page_add
                page = requests.get(page_add) #送出粉絲頁的requests
                page_soup = BeautifulSoup(page.text)
#                print page_soup
                page_id = page_soup.select('#pagelet_timeline_main_column') #選取含有粉絲頁id的dom
#                print page_id
                for p in page_id:
                    userlikes.write(user_id + ',' + p['data-gt'].split('"')[3] + '\n') #將粉絲id及粉絲頁id寫進檔案裡
                
            likes_hiddenItem = likes.select('.hiddenItem a') ##選取第三個部分的like
            for page in likes_hiddenItem:
                page_add = page['href']
#                print page
                page = requests.get(page_add) #送出粉絲頁的requests
                page_soup = BeautifulSoup(page.text)
#                print page_soup
                page_id = page_soup.select('#pagelet_timeline_main_column') #選取含有粉絲頁id的dom
#                print page_id
                for p in page_id:
                    userlikes.write(user_id + ',' + p['data-gt'].split('"')[3] + '\n') #將粉絲id及粉絲頁id寫進檔案裡
            
            userlikes.close()    
        
            print 'done' 
            
        else:
            print "not found"
        
            
    fans_file.close()