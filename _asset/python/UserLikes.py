# -*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup
from FacebookCrawler import FacebookCrawler

reload(sys)
sys.setdefaultencoding("utf-8")

# 為了不用重新再寫一次設定 cookie 和登入的程式，直接繼承 FacebookCrawler
class UserLikes(FacebookCrawler):

    src_file = '../data/fan_list_0_00000.csv'    # 要讀取的檔案名稱
    target_file = '../data/fan_list_0_00000.csv' # 要寫入的檔案名稱

    def __init__(self, segment_number):

        # Python 的繼承建構子寫法
        super(UserLikes, self).__init__()
        # 設定要讀取的檔案名稱
        self.src_file = '../data/fan_list/fan_list_' + str(self.fan_page_id) + '_' + str('%05d' %segment_number) + '.csv'
        # 設定要寫入的檔案名稱
        self.target_file = '../data/user_likes/user_likes_' + str(self.fan_page_id) + '_' + str('%05d' %segment_number) + '.csv'

        # 如果要讀取的檔案不存在就終止程式
        if not os.path.isfile(self.src_file):
            print self.src_file + ' not exists!'
            sys.exit()
        # 先把要寫入的檔案清空
        target_file = open(self.target_file, 'w')
        target_file.write('')
        target_file.close()
        # 上述動作都執行完畢後再做登入的動作
        self.login()

    def get_user_likes_first_page(self, user_id, html):

        # 找到點過讚的粉絲團清單的段落，去頭去尾取出要的部份
        page_list = '<ul class="' + html.split('<!-- <ul class="')[1].split('-->')[0]
        # 把取出的段落丟進 BeautifulSoup 函式，這樣才能使用 .select
        soup = BeautifulSoup(page_list)
        # 找到每個粉絲頁的連結
        links = soup.select('.fsl a')
        # 打開要寫入的目標檔案
        target_file = open(self.target_file, 'a')
        # 因為 select 的結果是 list，所以要跑 for 迴圈
        for link in links:
            # 連結 <a> 標籤裡有個 data-gt 屬性，值是一個 json，裡面的 engagement -> eng_tid 就是粉絲團 id
            page_id = json.loads(link['data-gt'])['engagement']['eng_tid'].encode('utf-8')
            # 把使用者 id 跟粉絲團 id 當成一筆資料寫成一行
            target_file.write(user_id + ',' + page_id + '\n')
        # 每個粉絲頁的資料都寫完以後把檔案關閉
        target_file.close()

    def get_user_likes(self, user_id, html):

        collection_token = html.split('<script>bigPipe.beforePageletArrive("pagelet_timeline_app_collection_')[1].split('")</script>')[0]

        cursor_code = html.split('"]],["Hovercard"],')[0]
        cursor = cursor_code[cursor_code.rfind('"') + 1:]

        # 打開要寫入的目標檔案
        target_file = open(self.target_file, 'a')
        while True:
            data_param = '{"collection_token":"' + collection_token + '","cursor":"' + cursor + '","tab_key":"likes","profile_id":' + user_id + ',"overview":false,"ftid":null,"order":null,"sk":"likes","importer_state":null}'
            target_url = 'https://www.facebook.com/ajax/pagelet/generic.php/LikesWithFollowCollectionPagelet?data=' + urllib2.quote(data_param) + '&__user=' + str(self.admin_id) + '&__a=1'

            response = self.opener.open(target_url)
            html = response.read()
            j = json.loads(html.replace('for (;;);',''))
            soup = BeautifulSoup(j['payload'])
            links = soup.select('.fcb a')
            for link in links:
                page_id = json.loads(link['data-gt'])['engagement']['eng_tid'].encode('utf-8')
                # 把使用者 id 跟粉絲團 id 當成一筆資料寫成一行
                target_file.write(user_id + ',' + page_id + '\n')

            cursor_code = html.split('"]],["Hovercard"],')[0]
            cursor = cursor_code[cursor_code.rfind('"') + 1:]

            if '"TimelineAppCollection","enableContentLoader"' not in html:
                break
        # 每個粉絲頁的資料都寫完以後把檔案關閉
        target_file.close()

    def crawl(self):

        # 以讀取模式打開來源檔案
        src_file = open(self.src_file, 'r')
        # 讀取來源檔案裡的每一行
        for line in src_file.readlines():
            # 把每一行資料用 ',' 拆成 list
            data = line.strip().split(',')
            # list 的第一個元素是 user_id、第三個元素是使用者首頁網址
            user_id = data[0]
            user_profile_url = data[2]

            # 針對兩種不同類型的使用者首頁網址，「說讚的內容」頁的網址也會不一樣
            if str(user_id) in user_profile_url:
                likes_url = user_profile_url + '&sk=likes'
            else:
                likes_url = user_profile_url + '/likes'

            # 用物件自己的 opener 打開網址
            response = self.opener.open(likes_url)
            # 把網頁原始檔讀成字串
            html = response.read()
            # 如果網頁原始檔裡面有找到灰色的讚的圖示就代表使用者有開放「說讚的內容」頁
            if 'https://www.facebook.com/images/profile/timeline/app_icons/likes_24.png' in html:
                # 在螢幕上顯示目前處理進度（sys.stdout.write 跟 print 的差別在於前者不會換行）
                sys.stdout.write('\tGetting user ' + str(user_id) + ' likes page...')
                # 為了判別使用者有沒有開放「說讚的內容」頁，其實已經讀取到分頁第一頁的內容了，不需要再開網址抓取
                self.get_user_likes_first_page(user_id, html)
                if '"TimelineAppCollection","enableContentLoader"' in html:
                    # 分頁第二頁之後需要開網址抓取
                    self.get_user_likes(user_id, html)
                print('done')
            else:
                print '\tUser ' + str(user_id) + ' hide liks page!'
        # 來源檔案內每筆資料都讀完以後把檔案關閉
        src_file.close()
        print 'Script ended.\n'

if __name__ == '__main__':
    for segment_number in range(x, y):
        obj = UserLikes(segment_number)
        obj.crawl()
        del(obj)
