# -*- coding: utf-8 -*-
#20150120 20150210 20150211
#jhhuclaire@gmail.com
import requests
import json
from bs4 import BeautifulSoup

file_input_appID = 'appID.dat'
#appID.dat 檔案內有 App Token
#FB app 名稱 IIIFansPro
file_appID = open(file_input_appID,'r')
ACCESS_TOKEN = file_appID.readlines()[0].strip()
file_appID.close()
#打開app token 檔案 & 讀進App Token & 關閉檔案
file_input_user_likes_list = 'user_likes.list'
#user_likes.list 內有所有要輸入的 csv 檔案 ; 例如 user_likes_57613404340_1.csv
file_input_list=open(file_input_user_likes_list,'r')
#讀進 file_input_user_likes_list 裡面的所有檔案
#
### 以下 for 迴圈，開始處理 list 裡面每一個檔案
for user_likes_csv in file_input_list:
    print user_likes_csv
    fan_page_info_file_output = open('fan_page_info'+user_likes_csv.strip(),'w')
    #打開輸出檔案; 檔名為 "fan_page_info"＋輸入的 csv 檔名; 例如 fan_page_infouser_likes_57613404340_1.csv
    fans_like_id = open(user_likes_csv.strip(),'r')
    #打開並讀進user id and 粉絲團id
    fields_list = ['id','name','link','category','description']
    fields = ','.join(fields_list)
    #準備 url 的字串 ; 輸出的項目
    #
    #以下 for 迴圈處理每個 csv （user_likes_csv）裡的粉絲團id
    for line in fans_like_id.readlines():
        info = line.strip().split(",")
        # csv 檔（user_likes_csv）裡的user id and 粉絲團id
        base_url = 'https://graph.facebook.com/v2.2/%s' %info[1]
        # info[1] = 粉絲團id  ( info[0] = user id)
        url = base_url + '?fields=%s&access_token=%s' %(fields, ACCESS_TOKEN)
        # 結合 url 所有資訊
        content = requests.get(url)
        # 取得網頁內容
        json_content = "[" + json.dumps(content, indent=1).decode("utf-8").strip() + "]"
        json_data = json.loads(json_content)
        # 整理取得的 json 內容
        #
        # 以下迴圈處理輸出格式; 每筆粉絲團資料輸出後換下一行 ; 若有缺資料直接‘逗號’
        for attribute in json_data:
            for field in fields_list:
                if field == fields_list[len(fields_list)-1]:
                    try:
                        fan_page_info_file_output.write(''.join(attribute[field].encode('utf-8').split())+'\n')
                        #若輸出資料是最後一個項目 (description),則輸出項目內容並換行
                    except KeyError:
                        fan_page_info_file_output.write('\n')
                        #若此項目沒有資料,直接換行
                else:
                    try:
                        fan_page_info_file_output.write(attribute[field].encode('utf-8').strip() + ",")
                        #若輸出資料不是最後一個項目 (description),則輸出項目內容並“逗號”
                    except KeyError:
                        fan_page_info_file_output.write(',')
                        #若輸出資料不是最後一個項目也沒有資料,則直接輸出逗號

    fans_like_id.close()
    fan_page_info_file_output.close()
file_input_list.close()
# 關閉所有檔案
