# -*- coding:utf-8 -*-
import requests, sys
from bs4 import BeautifulSoup

import param
fan_page_id = param.fan_page_id

#用for迴圈依序讀取csv檔
for page in range(2,31): #要讀取的csv的檔名
    file_name = '../data/fan_list_' + str(fan_page_id) + '_' + str('%05d' %page) + '.csv' #檔名
    result_file_name = '../data/user_likes_' + str(fan_page_id) + '_' + str('%05d' %page) + '.csv'

    result_file = open(result_file_name, 'w')
    result_file.write('')
    result_file.close()

    result_file = open(result_file_name, 'a')

    fans_file = open(file_name, 'r') #開啟csv檔
    fans_info = fans_file.readlines() #逐行讀取檔案，每行為一個字串

    #用for迴圈抓取每行粉絲的頁面網址
    for line in range(0,len(fans_info)):
        pos_1 = fans_info[line].find(',',0) #找到第一個逗點位置
        pos_2 = fans_info[line].find(',',pos_1+1) #找到第二個逗點位置
        fans_add = fans_info[line][pos_2+1:] #從第二個逗點後的字串為要抓取的網址

        res = requests.get(fans_add)

        if res.status_code == 200:  #判斷網頁是否打得開，Response 200
                
            user_id = fans_info[line][0:pos_1] #從csv檔裡取得user id
            sys.stdout.write(user_id + ' is processing...')

            soup = BeautifulSoup(res.content)
            captcha = soup.select('#captcha')
            if len(captcha) > 0 :

                print 'banned!'

            else:

                html = res.text.split('<!-- ')[4].split('-->')[0] #將包含likes內容的dom的註解刪除
                likes = BeautifulSoup(html)

                #user的頁面本身沒有粉絲頁的id，必須要進入粉絲頁裡抓取id。likes區塊分三部分mediaPageName、visible、hiddenItem、
                likes_mediaPageName = likes.select('.mediaRowItem') #選取第一個部分的like
                for page in likes_mediaPageName:
                    page_id = ''
                    if 'l.facebook.com' not in page['href']:
                        page_add = page['href'].split('/')
                        page_id = page_add[len(page_add) - 1]
                    result_file.write(user_id + ',' + page['href'] + ',' + page_id + '\n') #將粉絲id及粉絲頁id寫進檔案裡

                likes_visible = likes.select('.visible a') #選取第二個部分的like
                for page in likes_visible:
                    page_id = ''
                    if 'l.facebook.com' not in page['href']:
                        page_add = page['href'].split('/')
                        page_id = page_add[len(page_add) - 1]
                    result_file.write(user_id + ',' + page['href'] + ',' + page_id + '\n') #將粉絲id及粉絲頁id寫進檔案裡

                likes_hiddenItem = likes.select('.hiddenItem a') ##選取第三個部分的like
                for page in likes_hiddenItem:
                    page_id = ''
                    if 'l.facebook.com' not in page['href']:
                        page_add = page['href'].split('/')
                        page_id = page_add[len(page_add) - 1]
                    result_file.write(user_id + ',' + page['href'] + ',' + page_id + '\n') #將粉絲id及粉絲頁id寫進檔案裡

                print 'done'

        else:
            print "not found"

    result_file.close()
    fans_file.close()