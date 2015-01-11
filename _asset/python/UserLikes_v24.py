# -*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup
from FacebookCrawler import FacebookCrawler

reload(sys)
sys.setdefaultencoding("utf-8")

class UserLikes(FacebookCrawler):

    src_file = '../data/fan_list_0_00000.csv'    # file to load user list
    target_file = '../data/fan_list_0_00000.csv' # file to save user likes list

    def __init__(self, segment_number):

        super(UserLikes, self).__init__()
        self.src_file = '../data/fan_list_' + str(self.fan_page_id) + '_' + str('%05d' %segment_number) + '.csv'
        self.target_file = '../data/user_likes_' + str(self.fan_page_id) + '_' + str('%05d' %segment_number) + '.csv'
        if not os.path.isfile(self.src_file):
            print self.src_file + ' not exists!'
            sys.exit()
        target_file = open(self.target_file, 'w')
        target_file.write('')
        target_file.close()
        self.login()

    def get_list_first_page(self, user_id, html):
        page_list = '<ul class="' + html.split('<!-- <ul class="')[1].split('-->')[0]
        soup = BeautifulSoup(page_list)
        links = soup.select('.fsl a')
        target_file = open(self.target_file, 'a')
        for link in links:
            page_id = json.loads(link['data-gt'])['engagement']['eng_tid'].encode('utf-8')
            target_file.write(user_id + ',' + page_id + '\n')
        target_file.close()

    def get_user_likes(self, user_id, page):

        # list length is 8
        # codes start from here...
        return

    def crawl(self):

        src_file = open(self.src_file, 'r')
        for line in src_file.readlines():
            data = line.strip().split(',')
            user_id = data[0]
            user_profile_url = data[2]

            if str(user_id) in user_profile_url:
                likes_url = user_profile_url + '&sk=likes'
                # music_url = user_profile_url + '&sk=music'
            else:
                likes_url = user_profile_url + '/likes'
                # music_url = user_profile_url + '/music'

            response = self.opener.open(likes_url)
            html = response.read()
            if 'https://www.facebook.com/images/profile/timeline/app_icons/likes_24.png' in html:
                sys.stdout.write('\tGetting user ' + str(user_id) + ' likes page...')
                self.get_list_first_page(user_id, html)
                self.get_user_likes(user_id, 2)
                print('done')
            else:
                # response = self.opener.open(music_url)
                # html = response.read()
                # if 'https://www.facebook.com/images/profile/timeline/app_icons/music_24.png' in html:
                #     sys.stdout.write('\tGetting user ' + str(user_id) + ' music page...')
                #     self.get_list_first_page(user_id, html)
                #     self.get_user_music(user_id, 2)
                #     print('done')
                # else:
                    print '\tUser ' + str(user_id) + ' is wicked.'
        src_file.close()
        print 'Script ended.\n'

if __name__ == '__main__':
    segment_number = 1
    obj = UserLikes(segment_number)
    obj.crawl()
    del(obj)