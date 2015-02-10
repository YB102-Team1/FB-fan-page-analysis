# -*- coding: utf-8 -*-
#20150120 20150210
#jhhuclaire@gmail.com
import requests
import json
from bs4 import BeautifulSoup

file00='appID.dat'
ACCESS_TOKEN = open(file00,'r').readlines()[0].strip()
print ACCESS_TOKEN
fin01='user_likes_57613404340_1.csv'
fout01='fan_page_info'+fin01
foutput01 = open(fout01, 'w')
finput01 = open(fin01,'r')
for line in finput01.readlines():
    info = line.strip().split(",")
    print info[1]
    base_url = 'https://graph.facebook.com/v2.2/%s'%info[1]
    fields = 'id,name,link,category,description'
    field = fields.split(",") # each field for j loop
    url = '%s?fields=%s&access_token=%s' % \
    (base_url, fields, ACCESS_TOKEN,)
# Interpret the response as JSON and convert back
# to Python data structures
    content = requests.get(url).json()
#print content.encode("utf-8")
# Pretty-print the JSON and display it
    js = json.dumps(content, indent=1)
    jsd = js.decode('utf-8').strip()
    jsdlist= "[%s]"%jsd # add [] in the text of jsd for json
    locations = json.loads(jsdlist)
    for i in locations:       
        for j in field:
            if j == field[len(field)-1]:
                try:
                    foutput01.write(''.join(i[j].encode('utf-8').split())+'\n')
                except KeyError:
                    foutput01.write('\n')
            else:
                try:
                    foutput01.write(i[j].encode('utf-8').strip() + ",")
                except KeyError:
                    foutput01.write(',')

finput01.close()
foutput01.close()
