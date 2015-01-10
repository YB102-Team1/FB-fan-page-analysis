# -*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import socks, socket
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup

class FacebookCrawler(object):

    fan_page_id = 57613404340
    admin_id = 100000597488537
    admin_email = 'samas0120@gmail.com'
    admin_pwd = 'xup6u4vu;6'

    def __init__(self):

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [
            ('Referer', 'http://facebookcorewwwi.onion/login.php'),
            # ('Referer', 'http://login.facebook.com/login.php'),
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')
        ]
        self.opener = opener

    def login(self):

        url = 'https://facebookcorewwwi.onion/login.php?login_attempt=1'
        # url = 'https://login.facebook.com/login.php?login_attempt=1'
        data = "locale=en_US&non_com_login=&email="+self.admin_email+"&pass="+self.admin_pwd+"&lsd=20TOl"
        response = self.opener.open('http://facebookcorewwwi.onion')
        # response = self.opener.open('http://www.facebook.com')
        response = self.opener.open(url, data)
        if "Logout" in response.read():
            print "Login successfully.\n"
            a = response.read()
            if "logout" in a:
                print "Login successfully.\n"
                return a
        else:
            print "Failed login."
            print response.read()
            sys.exit()

if __name__ == '__main__':
    obj = FacebookCrawler()
    obj.login()
    url = 'https://facebookcorewwwi.onion/browse/?type=page_fans&page_id=' + str(obj.fan_page_id)
    # url = 'https://www.facebook.com/browse/?type=page_fans&page_id=' + str(obj.fan_page_id)
    response = obj.opener.open(url)
    html = response.read()
    soup = BeautifulSoup(html)
    fans = soup.select('.uiProfileBlockContent')
    print 'Found ' + str(len(fans)) + ' fans.'
    target_file = open('../data/test_crawler.csv', 'w')
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
                # row.append(user_profile + '&sk=likes')
            else:
                user_profile = a['href'].replace('?fref=pb&hc_location=profile_browser', '')
                row.append(user_profile)
                # row.append(user_profile + '/likes')
            target_file.write(','.join(row) + '\n')
    target_file.close()
    next_page = soup.select('.morePager')
    for link in next_page:
        next_page_url = 'https://facebookcorewwwi.onion' + link.find('div').find('a')['href'] + '&__user=' + str(obj.admin_id) + '&__a=1&__rev=1552948'
        # next_page_url = 'https://www.facebook.com' + link.find('div').find('a')['href'] + '&__user=' + str(obj.admin_id) + '&__a=1&__rev=1552948'
    print '\nNext page url:\n' + next_page_url + '\n'