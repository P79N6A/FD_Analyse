from datetime import date, timedelta
import xlrd
import json
from os.path import isfile, join, isdir
from os import listdir

def find_report_by_uins():
    crash_file_folder = "D:\Work\FD\Crash\CrashList.xls"
    data = xlrd.open_workbook(crash_file_folder)
    table = data.sheets()[0]
    nrows = table.nrows
    uin_list = []
    for i in range(nrows ):
        uin_list.append(table.cell(i,2).value)

    print(uin_list)

    st = date.today() - timedelta(4)
    et = date.today() - timedelta(1)
    cur_t = st;
    while cur_t <= et:
        file_path = "D:\Work\FD\Json\\" + str(cur_t) + ".json"
        file = open(file_path, "r")
        load_json = json.load(file)
        for item in load_json:
            params = str(item['getparams'])
            spilt_st = params.split(',')
            for sp_item in spilt_st:
                if sp_item.find(str("uin")) >= 0:
                    sp_ag = sp_item.split(':')
                    uin = sp_ag[1].strip('"')
                    found = False
                    for i_uin in uin_list:
                        if uin == str(i_uin):
                            found = True
                            print(str.format("uin:{0} find match", uin))
                    if not found:
                        print(str.format("uin:{0} not find", uin))

        cur_t = cur_t + timedelta(1)

def find_report_by_uin(uin_to_find, date_time):
    folder_path = "D:\Work\FD\Params\\"+ str(date_time)
    for f in listdir(folder_path):
        absolute_path = str.format("{0}\\{1}", folder_path, f)
        if isfile(absolute_path) and absolute_path.endswith('.txt'):
            file = open(absolute_path, "r", encoding='utf-8')
            load_json = json.load(file)
            uin = load_json['uin']
            if uin == str(uin_to_find):
                print(str.format("find match, file:{0}", f))


def find_report_by_uins_new(date_time):
    crash_file_folder = "D:\Work\FD\Crash\CrashList.xls"
    data = xlrd.open_workbook(crash_file_folder)
    table = data.sheets()[0]
    nrows = table.nrows
    uin_list = []
    for i in range(nrows ):
        uin_list.append(table.cell(i,2).value)

    print(uin_list)

    folder_path = "D:\Work\FD\Params\\"+ str(date_time)
    for f in listdir(folder_path):
        absolute_path = str.format("{0}\\{1}", folder_path, f)
        if isfile(absolute_path) and absolute_path.endswith('.txt'):
            file = open(absolute_path, "r", encoding='utf-8')
            load_json = json.load(file)
            uin = load_json['uin']
            found = False
            for i_uin in uin_list:
                if uin == str(i_uin):
                    found = True
                    print(str.format("uin:{0} find match {1}", uin, file.name))
                    break