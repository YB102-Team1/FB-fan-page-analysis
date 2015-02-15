# -*- coding:utf-8 -*-
# __author__ = 'Samas Lin<samas0120@gmail.com>'
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class UserLikesListMaker(object):

    fan_page_id = 0  # 粉絲團編號

    def __init__(self):

        import param
        self.fan_page_id = param.fan_page_id
        target_file = open('../data/user_likes.list', 'w')
        target_file.write('')
        target_file.close()

    def run(self, segment_limit):

        source_file_prefix = '../data/user_likes/user_likes_' + str(self.fan_page_id) + '_'

        target_file = open('../data/user_likes.list', 'r')
        result = target_file.read()
        target_file.close()

        for i in range(1, segment_limit + 1):
            source_file_name = source_file_prefix + str('%05d' %segment_limit) + '.csv'
            source_file = open(source_file_name, 'r')
            print str('segment %d:' %i)
            for data in source_file.readlines():
                fan_page_path = data.replace('\n', '').split(',')[2]
                if (fan_page_path not in result) and (fan_page_path != ''):
                    result = result + fan_page_path + '\n'
            source_file.close()

        target_file = open('../data/user_likes.list', 'w')
        result = target_file.write(result)
        target_file.close()

if __name__ == '__main__':
    user_likes_list_maker = UserLikesListMaker()
    user_likes_list_maker.run(1)