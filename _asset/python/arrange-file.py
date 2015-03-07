# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import param
fan_page_id = param.fan_page_id

def arrange_file(file_prefix, file_number):

    print('processing segment ' + str(file_number) + ':')
    file_name = '../data/' + file_prefix + '/' + file_prefix + '_' + str(fan_page_id) + '_' + str('%05d' %file_number) + '.csv'
    temp_content = ''
    line_index = 1;

    input_file = open(file_name, 'r')
    for line in input_file.readlines():
        if line not in temp_content:
            temp_content = temp_content + line
        else:
            print(str('file %d line %d repeat!' %(file_number, line_index)))
        line_index = line_index + 1
    input_file.close

    output_file = open(file_name, 'w')
    output_file.write(temp_content)
    output_file.close
    print('finished\n')

if __name__ == '__main__':
    # for file_number in range(1, 488):
    #     arrange_file('fan_list', file_number)

    for file_number in range(1, 14):
        arrange_file('user_likes', file_number)

    # for file_number in range(81,83):
    #     arrange_file('user_likes', file_number)

    # for file_number in range(161,163):
    #     arrange_file('user_likes', file_number)

    # arrange_file('user_likes', 241)

    # arrange_file('user_likes', 321)

    # for file_number in range(401,403):
    #     arrange_file('user_likes', file_number)