# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import param
fan_page_id = param.fan_page_id

def arrange_segment(file_prefix, segment_number):

	sys.stdout.write('processing segment ' + str(segment_number) + '......')
	source_file = '../data/' + file_prefix + '/' + file_prefix + '_' + str(fan_page_id) + '_' + str('%05d' %segment_number) + '.csv'
	target_file = '../data/' + file_prefix + '/' + file_prefix + '_' + str(fan_page_id) + '_' + str('%05d' %(segment_number + 1))+ '.csv'
	temp_content = ''

	input_file = open(source_file, 'r')
	file_content = input_file.read()
	input_file.close()

	next_file = open(target_file, 'r')
	for line in next_file.readlines():
		if line not in file_content:
			temp_content = temp_content + line
	next_file.close()

	next_file = open(target_file, 'w')
	next_file.write(temp_content)
	next_file.close()
	print('done')

if __name__ == '__main__':
	for segment_number in range(1,487):
		arrange_segment('fan_list', segment_number)