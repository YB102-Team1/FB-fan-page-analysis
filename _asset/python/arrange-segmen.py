# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def arrange_segment(segment_number):

	source_file = 'C:\\Users\\BigData\\fan_list_' + '57613404340' + '_' + str('%05d' %segment_number) + '.csv'#segment_number

	target_file = 'C:\\Users\\BigData\\fan_list_' + '57613404340' + '_' + str('%05d' %(segment_number + 1))+ '.csv'#segment_number + 1

	
	temp_content = ''            
	
	if segment_number == 1:
		input_file = open(source_file, 'r') 
		file_content = input_file.read()
		input_file.close()
	else:
		file_content = temp_content

	next_file = open(target_file, 'r') 
	for line in next_file.readlines():
		if line not in file_content:
			temp_content = temp_content + line
	next_file.close()

	next_file = open(target_file, 'w')
	next_file.write(temp_content)
	next_file.close()


if __name__ == '__main__':
	for segment_number in range(1,487):
		arrange_segment(segment_number)