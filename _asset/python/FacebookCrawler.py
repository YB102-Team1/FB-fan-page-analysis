# __author__ = 'Samas Lin<samas0120@gmail.com>'
import urllib2, cookielib, re, os, sys, json
from bs4 import BeautifulSoup

class Facebook():

    page_count = 1

    def __init__(self, email, password):

        self.email = email
        self.password = password
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [
            ('Referer', 'http://login.facebook.com/login.php'),
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')
        ]
        self.opener = opener

    def login(self):

        url = 'https://login.facebook.com/login.php?login_attempt=1'
        data = "locale=en_US&non_com_login=&email="+self.email+"&pass="+self.password+"&lsd=20TOl"
        usock = self.opener.open('http://www.facebook.com')
        usock = self.opener.open(url, data)
        if "Logout" in usock.read():
            print "Logged in."
            a = usock.read()
            if "logout" in a:
                print "Logged in."
                return a
        else:
            print "failed login"
            print usock.read()
            sys.exit()

    def claw(self, url):

        self.login()
        usock = self.opener.open(url)
        content = usock.read()
        result = BeautifulSoup(content)
        fans = result.select('.uiProfileBlockContent')
        print 'Page ' + str(self.page_count) + ' found ' + str(len(fans)) + ' fans.'
        fid = open('data.txt', 'w')
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
                fid.write(','.join(row) + '\n')
        fid.close()
        print 'Page ' + str(self.page_count) + ' finished.'
        self.page_count = self.page_count + 1
        self.next_page(result)

    def next_page(self, html):

        next_page = html.select('.morePager')
        for link in next_page:
            next_page_url = 'https://www.facebook.com' + link.find('div').find('a')['href'] + '&__user=100000597488537&__a=1&__rev=1552948'
        usock = self.opener.open(next_page_url)
        content_list = usock.read().replace('for (;;);{"__ar":1,"payload":null,"domops":[["appendContent","^div.fbProfileBrowserListContainer",true,', '').split('}')
        content = json.loads(content_list[0] + '}')['__html'].encode('utf-8')
        result = BeautifulSoup(content)
        fans = result.select('.uiProfileBlockContent')
        print 'Page ' + str(self.page_count) + ' found ' + str(len(fans)) + ' fans.'
        if len(fans) != 0:
            fid = open('data.txt', 'a')
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
                    fid.write(','.join(row) + '\n')
            fid.close()
            print 'Page ' + str(self.page_count) + ' finished.'
            self.page_count = self.page_count + 1
            # self.next_page(result)
        else:
            print 'script ended.'

if __name__ == '__main__':
    f = Facebook("samas0120@gmail.com", "xup6u4vu;6")
    f.claw('https://www.facebook.com/browse/?type=page_fans&page_id=57613404340')