#-*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup
from FacebookCrawler import FacebookCrawler

class FansList(FacebookCrawler):

    segment_size = 40
    start_offset = 0
    current_cursor = 0
    last_offset = 20
    target_file = 'fan_list_0.txt'

    def set_segment(self, segment_number):
        self.start_offset = (segment_number - 1) * self.segment_size
        self.current_cursor = (segment_number - 1) * self.segment_size
        self.last_offset = segment_number * self.segment_size - 20
        self.target_file = 'fan_list_' + str(segment_number) + '.txt'
        target_file = open(self.target_file, 'w')
        target_file.write('')
        target_file.close()

    def crawl(self, url):

        usock = self.opener.open(url)
        content_list = usock.read().replace('for (;;);{"__ar":1,"payload":null,"domops":[["appendContent","^div.fbProfileBrowserListContainer",true,', '').split('}')
        content = json.loads(content_list[0] + '}')['__html'].encode('utf-8')
        soup_content = BeautifulSoup(content)
        fans = soup_content.select('.uiProfileBlockContent')
        sys.stdout.write('Getting fans ' + str(self.current_cursor) + '-' + str(self.current_cursor + 20) + ' ...')
        target_file = open(self.target_file, 'a')
        for fan in fans:
            alink = fan.select('.fcb a')
            row = []
            for a in alink:
                user_fb_id = a.parent.parent.parent.parent.parent.parent.parent['id'].replace('adminableItem_', '')
                row.append(user_fb_id)
                user_name = a.text.encode('utf-8')
                row.append(user_name)
                if user_fb_id in a['href']:
                    user_profile = a['href'].replace('&fref=pb&hc_location=profile_browser', '')
                    row.append(user_profile)
                else:
                    user_profile = a['href'].replace('?fref=pb&hc_location=profile_browser', '')
                    row.append(user_profile)
                target_file.write(','.join(row) + '\n')
        target_file.close()
        print 'done.'
        self.current_cursor = self.current_cursor + 20
        next_page = soup_content.select('.morePager')
        if len(next_page) == 0 or self.current_cursor > self.last_offset:
            print 'script ended.'
        else :
            for link in next_page:
                next_page_url = 'https://www.facebook.com' + link.find('div').find('a')['href'] + '&__user=100000597488537&__a=1&__rev=1552948'
            self.crawl(next_page_url)

if __name__ == '__main__':

    segment_number = 1
    user_email = 'samas0120@gmail.com'
    user_pwd = 'xup6u4vu;6'
    fan_page_id = 57613404340

    f = FansList(user_email, user_pwd)
    f.set_segment(segment_number)

    f.login()
    url = 'https://www.facebook.com/ajax/browser/list/page_fans/?dge=public_profile%3Afbpage_to_user&start=0&__user=100000597488537&__a=1&__rev=1552948&page_id=' + str(fan_page_id)
    f.crawl(url)