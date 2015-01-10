# -*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup
from FacebookCrawler import FacebookCrawler

class FansList(FacebookCrawler):

    segment_size = 40                        # users in a segment
    start_offset = 0                         # start offset of this segment
    last_offset = 20                         # end offset of this segment
    target_file = '../data/fan_list_0_0.csv' # file to save user list

    def __init__(self, segment_number):

        super(FansList, self).__init__()
        self.start_offset = (segment_number - 1) * self.segment_size
        self.last_offset = segment_number * self.segment_size - 20
        self.target_file = '../data/fan_list_' + str(self.fan_page_id) + '_' + str(segment_number) + '.csv'
        target_file = open(self.target_file, 'w')
        target_file.write('')
        target_file.close()
        self.login()

    def crawl(self, page):

        start = self.start_offset + (page - 1) * 20
        url = 'https://www.facebook.com/ajax/browser/list/page_fans/?dge=public_profile%3Afbpage_to_user&__user=100000597488537&__a=1&__rev=1552948&start=' + str(start) + '&page_id=' + str(self.fan_page_id)
        response = self.opener.open(url)
        json_content = response.read().replace('for (;;);{"__ar":1,"payload":null,"domops":[["appendContent","^div.fbProfileBrowserListContainer",true,', '').split('}')
        html = json.loads(json_content[0] + '}')['__html'].encode('utf-8')
        soup = BeautifulSoup(html)
        fans = soup.select('.uiProfileBlockContent')
        sys.stdout.write('Getting fans ' + str(start) + '-' + str(start + 20) + ' ...')
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
        print 'done'
        next_page = soup.select('.morePager')
        if len(next_page) == 0 or start + 20 > self.last_offset:
            print '\nScript ended.\n'
        else :
            self.crawl(page + 1)

if __name__ == '__main__':
    segment_number = 1
    obj = FansList(segment_number)
    obj.crawl(1)