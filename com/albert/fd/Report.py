__author__ = 'alberthe'

from os.path import isfile, join, isdir
from os import listdir
from com.albert.fd.visit import get_save_path, get_copy_path, get_suspicious_path, get_report_config_path, get_report_output_path, get_report_ignore_path
import shutil
from com.albert.fd.count_line import stats_tree
import os
import sys

class report_data:
    cnt = 0
    path_list = []
    count_list = []

    def __init__(self):
        self.cnt = 0
        self.path_list = []
        self.count_list = []

class report_data_by_version:
    version = ''
    revision = ''
    res_list = {}
    new_list = {}

    def __init__(self, version, revision):
        self.version = version
        self.revision = revision
        self.res_list = {}
        self.new_list = {}
        for item in config_list:
            self.res_list[item] = report_data()

final_report_data = {}

report_version = '7.7.8.3705'
report_revision = '366328'
config_list = []
ignore_list = []
#report_res_list = {}
#report_new_list = {}

i_list = {1, 2}
version_list = {1:'7.7.8.3705', 2:'7.7.5.3680'}
revision_list = {1:'366328', 2:'365333'}

def load_report_config():
    cfg_path = get_report_config_path()
    cfg_file = open(cfg_path, "r", encoding='utf-8')
    for line in cfg_file:
        line = line.strip('\n')
        config_list.append(line)

def load_report_ignore():
    cfg_path = get_report_ignore_path()
    cfg_file = open(cfg_path, "r", encoding='utf-8')
    for line in cfg_file:
        line = line.strip('\n')
        ignore_list.append(line)

def in_ignore_list(target_item):
    for item in ignore_list:
        if str(target_item).find(item) >= 0:
            return True
    return False

def in_monitor_list(last_line):
    for i in i_list:
        cur_ver = version_list[i]
        cur_rev = revision_list[i]
        if str(last_line).find(cur_ver) >= 0 and str(last_line).find(cur_rev) >= 0:
            return cur_ver, cur_rev
    return '', ''

def iterate_fd_list(folder):
    for f in listdir(folder):
        absolute_path = str.format("{0}\\{1}", folder, f)
        if isdir(absolute_path):
           iterate_fd_list(absolute_path)
        elif isfile(absolute_path):
            if absolute_path.endswith('.txt'):
                txt_file = open(absolute_path, "r", encoding='utf-8')
                last_line = ""
                tmp_count_list = {}
                for item in config_list:
                    tmp_count_list[item] = 0
                tree = stats_tree()
                for line in txt_file:
                    line = line.strip('\n')
                    tree.add_to_tree(line)
                    last_line = line
                    for item in config_list:
                        if str(line).find(item) >= 0:
                            tmp_count_list[item] = tmp_count_list[item] + 1
                # print(absolute_path)
                # for item in tmp_count_list:
                #     print(str.format("key:{0}, value:{1}", item, tmp_count_list[item]))
                # pause = input(str.format("need continue?"))
                cur_ver, cur_rev = in_monitor_list(last_line)
                if cur_ver != '' and cur_rev != '':
                    cur_key = cur_ver + cur_rev
                    print(cur_key)
                    if not cur_key in final_report_data:
                        final_report_data[cur_key] = report_data_by_version(cur_ver, cur_rev)
                    cur_final_data = final_report_data[cur_key]

                    for item in tmp_count_list:
                        if tmp_count_list[item] > 100:
                            if not item in cur_final_data.res_list:
                                cur_final_data.res_list[item] = report_data()

                            cur_data = cur_final_data.res_list[item]
                            #cur_data =report_res_list[item]
                            cur_data.cnt = cur_data.cnt + 1
                            cur_data.path_list.append(absolute_path)
                            cur_data.count_list.append(tmp_count_list[item])

                    ret_data = tree.get_traverse_data()
                    item_handle_set = set()
                    for item_data in ret_data:
                        if not in_ignore_list(item_data) and ret_data[item_data] > 100 and not (item_data in item_handle_set) :
                            item_handle_set.add(item_data)
                            if not item_data in cur_final_data.new_list:
                                cur_final_data.new_list[item_data] = report_data()
                            cur_data = cur_final_data.new_list[item_data]
                            cur_data.cnt = cur_data.cnt + 1
                            cur_data.path_list.append(absolute_path)
                            cur_data.count_list.append(ret_data[item_data])
                            #print('new %s, %s has %s line'%(item_data, absolute_path, ret_data[item_data]))
                            #pause = input(str.format("need continue?"))
                txt_file.close()

                # for item in report_res_list:
                #     print(str.format("key:{0}, value:{1}", item, report_res_list[item]))
                # pause = input(str.format("need continue?"))

def generate_report():
    save_folder = get_save_path()
    load_report_config()
    load_report_ignore()
    iterate_fd_list(save_folder)

    output_path = get_report_output_path()
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    output_file_path = os.path.join(output_path, "report.txt")
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    f_res = open(output_file_path, 'w')
    output_new_path = os.path.join(output_path, "report_new.txt")
    if os.path.exists(output_new_path):
        os.remove(output_new_path)
    f_new = open(output_new_path, 'w')

    for i in i_list:
        cur_ver = version_list[i]
        cur_rev = revision_list[i]
        cur_key = cur_ver + cur_rev
        f_res.write("\nversion:%s, revision:%s\n" % (cur_ver, cur_rev))
        if not cur_key in final_report_data:
            continue
        cur_report_data = final_report_data[cur_key]
        for item in cur_report_data.res_list:
            cur_data = cur_report_data.res_list[item]
            f_res.write('fd desc:%s, time:%s\n' % (item, cur_data.cnt))
        for item in cur_report_data.res_list:
            cur_data = cur_report_data.res_list[item]
            f_res.write("\n%s:\n" % item)
            for path, count in zip(cur_data.path_list, cur_data.count_list):
                f_res.write("%s has %s lines\n" % (path, count))

        for item in cur_report_data.new_list:
            cur_data = cur_report_data.new_list[item]
            f_new.write("\n%s:\n" % item)
            for path, count in zip(cur_data.path_list, cur_data.count_list):
                f_new.write("%s has %s lines\n" % (path, count))

    f_res.close()
    f_new.close()