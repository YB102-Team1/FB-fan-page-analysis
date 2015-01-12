# -*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

class FacebookCrawler(object):

    fan_page_id = 57613404340           # 八三夭粉絲團編號
    admin_id = 100000597488537          # 管理員帳號編號
    admin_email = 'samas0120@gmail.com' # 管理員帳號
    admin_pwd = 'xup6u4vu;6'            # 管理員密碼

    def __init__(self):

        # 因為需要使用 cookie 登入
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [
            ('Referer', 'http://login.facebook.com/login.php'),
            ('Content-Type', 'application/x-www-form-urlencoded'),
            # 偽裝這隻爬蟲其實是用 Firefox 在瀏覽網頁
            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')
        ]
        self.opener = opener

    def login(self):

        url = 'https://login.facebook.com/login.php?login_attempt=1'
        data = "locale=en_US&non_com_login=&email="+self.admin_email+"&pass="+self.admin_pwd+"&lsd=20TOl"
        response = self.opener.open('http://www.facebook.com')
        response = self.opener.open(url, data)
        # 如果登入以後回傳的頁面有 "Logout" 或 "logout" 的字詞代表登入成功
        if "Logout" in response.read():
            print "Login successfully."
            a = response.read()
            if "logout" in a:
                print "Login successfully."
                return a
        else:
            print "Failed login."
            print response.read()
            sys.exit()

if __name__ == '__main__':
    # 建立一個 FacebookCrawler 類別的物件
    obj = FacebookCrawler()
    # 登入
    obj.login()
    # 要打開的網址
    url = 'https://www.facebook.com/browse/?type=page_fans&page_id=' + str(obj.fan_page_id)
    # 用 FacebookCrawler 物件的 opener 打開網址
    response = obj.opener.open(url)
    # 把網頁原始檔讀成字串
    html = response.read()
    # 把網頁原始檔丟進 BeautifulSoup 函式，這樣才能使用 .select
    soup = BeautifulSoup(html)
    # 取得每個粉絲區塊
    fans = soup.select('.uiProfileBlockContent')
    print 'Found ' + str(len(fans)) + ' fans.'
    # 打開要寫入的檔案
    target_file = open('../data/test_crawler.csv', 'w')
    # 因為 select 的結果是 list，所以要跑 for 迴圈
    for fan in fans:
        # 找到粉絲區塊裡面的連結
        alink = fan.select('.fsl.fwb.fcb a')
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
            target_file.write(','.join(row) + '\n')
    # 每個粉絲的資料都寫完以後把檔案關閉
    target_file.close()
    # 找到包住下一頁連結的區塊
    next_page = soup.select('.morePager')
    # 因為 select 的結果是 list，所以要跑 for 迴圈
    for link in next_page:
        # 把找到的下一頁連結串成完整的網址
        next_page_url = 'https://www.facebook.com' + link.find('div').find('a')['href'] + '&__user=' + str(obj.admin_id) + '&__a=1&__rev=1552948'
    print '\nNext page url:\n' + next_page_url + '\n'