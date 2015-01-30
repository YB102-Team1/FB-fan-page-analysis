# -*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import sys, os, requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

class UserLikes(object):

    fan_page_id = 0                                # 粉絲團編號
    src_file = '../data/fan_list_0_00000.csv'      # 要讀取的檔案名稱
    target_file = '../data/user_likes_0_00000.csv' # 要寫入的檔案名稱

    def __init__(self, segment_number):

        # 讀取粉絲團編號
        import param
        self.fan_page_id = param.fan_page_id
        # 設定要讀取的檔案名稱
        self.src_file = '../data/fan_list_' + str(self.fan_page_id) + '_' + str('%05d' %segment_number) + '.csv'
        # 設定要寫入的檔案名稱
        self.target_file = '../data/user_likes_' + str(self.fan_page_id) + '_' + str('%05d' %segment_number) + '.csv'
        # 如果要讀取的檔案不存在就終止程式
        if not os.path.isfile(self.src_file):
            print self.src_file + ' not exists!'
            sys.exit()
        # 先把要寫入的檔案清空
        target_file = open(self.target_file, 'w')
        target_file.write('')
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

            # 用 requests 打開網址
            response = requests.get(likes_url);
            # 把網頁原始檔讀成字串
            html = response.content
            # 如果網頁原始檔裡面有找到「最愛」就代表使用者有開放「說讚的內容」頁
            if '<h4 class="uiHeaderTitle">最愛</h4>' in html:

                # 在螢幕上顯示目前處理進度（sys.stdout.write 跟 print 的差別在於前者不會換行）
                sys.stdout.write('\tGetting user ' + str(user_id) + ' likes page...')

                fx = open('result' + user_id + '.html', 'w')
                fx.write(html)
                fx.close()

                # soup = BeautifulSoup(html)
                # test = soup.select('.mediaPageName')
                # print test
                # for page_name in test:
                #     print page_name

                print('done')
            else:
                print '\tUser ' + str(user_id) + ' hide liks page!'
        # 來源檔案內每筆資料都讀完以後把檔案關閉
        src_file.close()
        print 'Script ended.\n'

if __name__ == '__main__':
    segment_number = 1
    obj = UserLikes(segment_number)
    obj.crawl()
    del(obj)