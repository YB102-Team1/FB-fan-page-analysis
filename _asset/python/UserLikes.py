#-*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup
from FacebookCrawler import FacebookCrawler

class UserLikes(FacebookCrawler):

    src_file = 'fan_list_0.txt'
    target_file = 'fan_list_0.txt'

    def set_segment(self, segment_number):
        self.src_file = 'fan_list_' + str(segment_number) + '.txt'
        self.target_file = 'user_likes_' + str(segment_number) + '.txt'
        if not os.path.isfile(self.src_file):
            print self.src_file + ' not exists!'
            sys.exit()
        else:
            target_file = open(self.target_file, 'w')
            target_file.write('')
            target_file.close()

    def crawl(self):

        src_file = open(self.src_file, 'r')
        for line in src_file.readlines():
            data = line.strip().split(',')
            user_id = data[0]
            user_profile_url = data[2]

            if str(user_id) in user_profile_url:
                likes_url = user_profile_url + '&sk=likes'
                music_url = user_profile_url + '&sk=music'
            else:
                likes_url = user_profile_url + '/likes'
                music_url = user_profile_url + '/music'

            usock = f.opener.open(likes_url)
            content = usock.read()
            if 'https://www.facebook.com/images/profile/timeline/app_icons/likes_24.png' in content:
                # codes strat from here...
                print 'User ' + str(user_id) + ' likes page:\n' + likes_url + '\n'
                # codes end at here...
            else:
                # codes strat from here...
                usock = f.opener.open(music_url)
                content = usock.read()
                if 'https://www.facebook.com/images/profile/timeline/app_icons/music_24.png' in content:
                    print 'User ' + str(user_id) + ' music page:\n' + music_url + '\n'
                else:
                    print 'User ' + str(user_id) + ' is wicked.\n'
                # codes end at here...

        src_file.close()

if __name__ == '__main__':

    segment_number = 1
    user_email = 'samas0120@gmail.com'
    user_pwd = 'xup6u4vu;6'

    f = UserLikes(user_email, user_pwd)
    f.set_segment(segment_number)

    f.login()
    f.crawl()