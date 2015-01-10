import socket  
# download http://sourceforge.net/projects/socksipy/
import socks
import httplib

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
    socket.socket = socks.socksocket
    
def main():
    connetTor():
        
        conn = httplib.HTTPConnection("http://www.myipaddress.com/show-my-ip-address/")
        conn.request("GET","/")
 response = conn.getresponse()
    
if  __name__ == "__main__";
    main()

# 洋蔥專用FB網址(沒開tor會連不上)
# https://facebookcorewwwi.onion/	

# Stem：a Python controller library for Tor(還沒研究)
# https://stem.torproject.org/

# 以下為網路上挖的還沒看完

import socks

s = socks.socksocket()

s.set_proxy(socks.SOCKS5, "localhost") # SOCKS4 and SOCKS5 use port 1080 by default
# Or
s.set_proxy(socks.SOCKS4, "localhost", 4444)
# Or
s.set_proxy(socks.HTTP, "5.5.5.5", 8888)

# Can be treated identical to a regular socket object
s.connect(("www.test.com", 80))
s.sendall("GET / ...")
print s.recv(4096)

import socket
import socks
import urllib2

socks.set_default_proxy(socks.SOCKS5, "localhost")
socket.socket = socks.socksocket

urllib2.urlopen("http://...") # All requests will pass through the SOCKS proxy

proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
    opener = urllib2.build_opener(proxy_support) 
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    print opener.open('http://www.google.com').read()

import urllib2
import httplib

from BeautifulSoup import BeautifulSoup
from time import sleep

class Scraper(object):
    def __init__(self, options, args):
        if options.proxy is None:
            options.proxy = "http://localhost:8118/"
        self._open = self._get_opener(options.proxy)

    def _get_opener(self, proxy):
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)
        return opener.open

    def get_soup(self, url):
        soup = None
        while soup is None:
            try:
                request = urllib2.Request(url)
                request.add_header('User-Agent', 'foo bar useragent')
                soup = BeautifulSoup(self._open(request))
            except (httplib.IncompleteRead, httplib.BadStatusLine,
                    urllib2.HTTPError, ValueError, urllib2.URLError), err:
                sleep(1)
        return soup

class PageType(Scraper):
    _URL_TEMPL = "http://foobar.com/baz/%s"

    def items_from_page(self, url):
        nextpage = None
        soup = self.get_soup(url)

        items = []
        for item in soup.findAll("foo"):
            items.append(item["bar"])
            nexpage = item["href"]

        return nextpage, items

    def get_items(self):
        nextpage, items = self._categories_from_page(self._START_URL % "start.html")
        while nextpage is not None:
            nextpage, newitems = self.items_from_page(self._URL_TEMPL % nextpage)
            items.extend(newitems)
        return items()

pt = PageType()
print pt.get_items()

