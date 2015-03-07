# -*- coding:utf-8 -*-
import requests, sys, os, time, random
from bs4 import BeautifulSoup

import param
fan_page_id = param.fan_page_id

import requesocks
session = requesocks.session()
session.proxies = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}
cookies = dict(datr='AW76VHI0KTVKEK2Zq9kcCKTG')
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18',
    'DNT':'1',
    'Cache-Control':'max-age=0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

#用for迴圈依序讀取csv檔
for page in range(13,14):

    #存放使用者清單的檔案名稱
    input_file_name = '../data/fan_list/fan_list_' + str(fan_page_id) + '_' + str('%05d' %page) + '.csv'
    #寫入使用者「說讚的內容」的檔案名稱
    output_file_name = '../data/user_likes/user_likes_' + str(fan_page_id) + '_' + str('%05d' %page) + '.csv'

    #如果要寫入的檔案不存在，就建立檔案
    if not os.path.isfile(output_file_name):
        result_file = open(output_file_name, 'w')
        result_file.write('')
        result_file.close

    #以附加模式打開要寫入的檔案
    result_file = open(output_file_name, 'a')

    #以讀取模式打開存放使用者清單的檔案
    input_file = open(input_file_name, 'r')
    lines = input_file.read().split('\n')[:-1]
    input_file.close()

    line_counter = 0

    print 'segment ' + str(page) + ' start:'

    #用for迴圈抓取每行資料
    for line in lines:

        #去除換行符號後用「,」把每行資料拆成list
        fan_data = line.replace('\n', '').split(',')
        user_id = fan_data[0]
        user_name = fan_data[1]
        user_url = fan_data[2]

        #用requests.get取得網頁內容
        res = requests.get(user_url, cookies=cookies, headers=headers)
        #user_url.replace('https://www.facebook.com', 'https://facebookcorewwwi.onion')

        #判斷網頁是否打得開，Response 200代表成功
        if res.status_code == 200:

            sys.stdout.write(user_id + ' is processing...')

            if 'Redirecting...' in res.text:
                user_url = 'https://zh-tw.facebook.com/people/' + user_name + '/' + user_id
                res = requests.get(user_url, cookies=cookies, headers=headers)

            soup = BeautifulSoup(res.content)

            #如果找到id為captcha的DOM代表被要求輸入驗證碼，跳過，並且保留「pending」狀態
            captcha = soup.select('#captcha')

            if len(captcha) > 0 :
                sys.stdout.write(' => captcha\nRetrying...')

            counter = 1
            while len(captcha) > 0 and counter <= 5 :
                sys.stdout.write('*')
                res = requests.get(user_url, cookies=cookies, headers=headers)
                soup = BeautifulSoup(res.content)
                captcha = soup.select('#captcha')
                counter = counter + 1

            if 'captcha' in res.text :
                print ' => banned!   ' + user_id
                input_file = open(input_file_name, 'w')
                lines = input_file.write('\n'.join(lines[line_counter:]) + '\n')
                input_file.close()
                break

            #將包含likes內容的dom的註解刪除
            try:
                html = res.text.split('<!-- ')[4].split('-->')[0]
            except Exception, e:
                print e.message

            likes = BeautifulSoup(html)

            #user的頁面本身沒有粉絲頁的id，必須要進入粉絲頁裡抓取id。likes區塊分三部分mediaPageName、visible、hiddenItem
            #選取第一個部分的like
            likes_mediaPageName = likes.select('.mediaRowItem')
            for page in likes_mediaPageName:
                page_id = ''
                if 'l.facebook.com' not in page['href']:
                    page_add = page['href'].split('/')
                    page_id = page_add[len(page_add) - 1]
                result_file.write(user_id + ',' + page['href'] + ',' + page_id + '\n')

            #選取第二個部分的like
            likes_visible = likes.select('.visible a')
            for page in likes_visible:
                page_id = ''
                if 'l.facebook.com' not in page['href']:
                    page_add = page['href'].split('/')
                    page_id = page_add[len(page_add) - 1]
                result_file.write(user_id + ',' + page['href'] + ',' + page_id + '\n')

            #選取第三個部分的like
            likes_hiddenItem = likes.select('.hiddenItem a')
            for page in likes_hiddenItem:
                page_id = ''
                if 'l.facebook.com' not in page['href']:
                    page_add = page['href'].split('/')
                    page_id = page_add[len(page_add) - 1]
                result_file.write(user_id + ',' + page['href'] + ',' + page_id + '\n')

            print ' => done'
            time.sleep(random.randrange(1,6))

        #Response 不是200代表使用者有設定隱私無法讀取
        else:
            print "not found"

        line_counter = line_counter + 1

    result_file.close()