# -*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup
from FacebookCrawler import FacebookCrawler

reload(sys)
sys.setdefaultencoding("utf-8")

# 為了不用重新再寫一次設定 cookie 和登入的程式，直接繼承 FansList
class FansList(FacebookCrawler):

    segment_size = 1000                          # 每個 segment（碎片，把粉絲以固定數量拆成好幾段碎片）裡面有幾個粉絲
    start_offset = 0                             # 這個 segment 的第一頁
    last_offset = 20                             # 這個 segment 的最後一頁
    target_file = '../data/fan_list/fan_list_0_00000.csv' # 這個 segment 的資料會寫入哪個檔案

    def __init__(self, segment_number):

        # Python 的繼承建構子寫法
        super(FansList, self).__init__()
        # 設定這個 segment 的第一頁
        self.start_offset = (segment_number - 1) * self.segment_size
        # 設定這個 segment 的最後一頁
        self.last_offset = segment_number * self.segment_size - 20
        # 設定這個 segment 要寫入的檔案名稱
        self.target_file = '../data/fan_list/fan_list_' + str(self.fan_page_id) + '_' + str('%05d' %segment_number) + '.csv'
        # 先把要寫入的檔案清空
        target_file = open(self.target_file, 'w')
        target_file.write('')
        target_file.close()
        # 上述動作都執行完畢後再做登入的動作
        self.login()

    def crawl(self, page):

        # 設定網址的 start 參數
        start = self.start_offset + (page - 1) * 20
        # 把參數放進要取得的 url
        url = 'https://www.facebook.com/ajax/browser/list/page_fans/?dge=public_profile%3Afbpage_to_user&__user=100000597488537&__a=1&__rev=1552948&start=' + str(start) + '&page_id=' + str(self.fan_page_id)
        # 用物件自己的 opener 打開網址
        response = self.opener.open(url)
        # 因為真正的粉絲清單藏在一個很像 json 格式的段落中間，先把要取的段落取出來
        json_content = response.read().replace('for (;;);{"__ar":1,"payload":null,"domops":[["appendContent","^div.fbProfileBrowserListContainer",true,', '').split('}')
        # 把取出的段落當成 json 讀取、解碼，取得裡面 key 為 "__html" 的資料
        html = json.loads(json_content[0] + '}')['__html'].encode('utf-8')
        # 把內容丟進 BeautifulSoup 函式，這樣才能使用 .select
        soup = BeautifulSoup(html)
        # 取得每個粉絲區塊
        fans = soup.select('.uiProfileBlockContent')
        # 在螢幕上顯示目前處理進度（sys.stdout.write 跟 print 的差別在於前者不會換行）
        sys.stdout.write('\tGetting fans ' + str(start) + '-' + str(start + 19) + ' ...')
        # 打開要寫入的檔案
        target_file = open(self.target_file, 'a')
        # 因為 select 的結果是 list，所以要跑 for 迴圈
        for fan in fans:
            # 找到粉絲區塊裡面的連結
            alink = fan.select('.fcb a')
            # 建立一個叫做 row 的空 list
            row = []
            # 因為 select 的結果是 list，所以要跑 for 迴圈
            for a in alink:
                # 在粉絲區塊的往上數第七層 div，會用 adminableItem_{user_id} 來當做 id 屬性，把 'adminableItem_' 去掉就是 user_id
                user_fb_id = a.parent.parent.parent.parent.parent.parent.parent['id'].replace('adminableItem_', '')
                # 把 user_id 加進 row 這個 list
                row.append(user_fb_id)
                # 每個連結 <a> 標籤中間夾的文字就是使用者名稱
                user_name = a.text.encode('utf-8')
                # 把使用者名稱加進 row 這個 list
                row.append(user_name)
                # 針對使用者首頁的網址把不需要的字串去掉，然後加入 row 這個 list
                if user_fb_id in a['href']:
                    user_profile = a['href'].replace('&fref=pb&hc_location=profile_browser', '')
                    row.append(user_profile)
                else:
                    user_profile = a['href'].replace('?fref=pb&hc_location=profile_browser', '')
                    row.append(user_profile)
                # 把 row 裡面的元素（user_id、使用者名稱、使用者首頁的網址）用 ',' 串接成字串，再加上一個換行符號後寫進檔案
                target_file.write(','.join(row).encode('utf-8') + '\n')
        # 每個粉絲的資料都寫完以後把檔案關閉
        target_file.close()
        print 'done'
        # 找到包住下一頁連結的區塊
        next_page = soup.select('.morePager')
        # 如果這個 segment 沒有下一頁連結、或是下一頁網址已經是下一個 segment 的範圍就停止
        if len(next_page) == 0 or start + 20 > self.last_offset:
            print 'Script ended.\n'
        # 否則就繼續抓下一頁
        else :
            self.crawl(page + 1)

if __name__ == '__main__':
    for segment_number in range(1, 601):
        obj = FansList(segment_number)
        print 'Crawling fans ' + str(obj.start_offset) + '-' + str(obj.last_offset + 19) + ':'
        obj.crawl(1)
        del(obj)