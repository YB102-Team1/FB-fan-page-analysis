# -*- coding: utf-8 -*-
#20150120 20150210 20150211
#jhhuclaire@gmail.com
import requests
import json
from bs4 import BeautifulSoup


file_input_appID = 'appID.dat'
file_appID = open(file_input_appID,'r')
ACCESS_TOKEN = file_appID.readlines()[0].strip()
file_appID.close()
file_input_user_likes_list = 'user_likes.list'
file_input_list=open(file_input_user_likes_list,'r')

for user_likes_csv in file_input_list:
    print user_likes_csv
    fan_page_info_file_output=open('fan_page_info'+user_likes_csv.strip(),'w')
    fans_like_id = open(user_likes_csv.strip(),'r')
    fields_list = ['id','name','link','category','description']
    fields = ','.join(fields_list) 
    for line in fans_like_id.readlines():
        info = line.strip().split(",")
        base_url = 'https://graph.facebook.com/v2.2/%s'%info[1]
        url = '%s?fields=%s&access_token=%s'%(base_url, fields, ACCESS_TOKEN,)
# Interpret the response as JSON and convert back
# to Python data structures
        content = requests.get(url).json()
#print content.encode("utf-8")
# Pretty-print the JSON and display it
        json_content = "[" + json.dumps(content, indent=1).decode("utf-8").strip() + "]"
        json_data = json.loads(json_content)
        for attribute in json_data:       
            for field in fields_list:
                if field == fields_list[len(fields_list)-1]:
                    try:
                        fan_page_info_file_output.write(''.join(attribute[field].encode('utf-8').split())+'\n')
                    except KeyError:
                        fan_page_info_file_output.write('\n')
                else:
                    try:
                        fan_page_info_file_output.write(attribute[field].encode('utf-8').strip() + ",")
                    except KeyError:
                        fan_page_info_file_output.write(',')


    fans_like_id.close()
    fan_page_info_file_output.close()
file_input_list.close()
