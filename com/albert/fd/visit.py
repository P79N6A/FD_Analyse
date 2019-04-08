import webbrowser
from datetime import date, timedelta
import time

sub_timedelta = 1

def set_timedelta(delta):
    global sub_timedelta
    sub_timedelta = int(delta)
    yesterday = date.today() - timedelta(sub_timedelta)
    print(yesterday)

def visit(delta):
    global sub_timedelta
    sub_timedelta = int(delta)
    yesterday = date.today() - timedelta(sub_timedelta)
    stime = str(yesterday) + ' 00:00:00'
    etime = str(yesterday) + ' 23:59:59'
    url = str.format("http://zzif.isd.com/zzthinkphp/index.php/Home/info/lists/stime/{0}/etime/{1}/p_id/1/plugin/19/type/json", stime, etime)
    webbrowser.open_new(url)

def get_report_config_path():
    return str("D:\Work\FD\Config\\report_cfg.txt")

def get_report_ignore_path():
    return str("D:\Work\FD\Config\\ignore_cfg.txt")

def get_report_output_path():
    global sub_timedelta
    day_time = date.today() - timedelta(sub_timedelta)
    ret_folder = str.format("D:\Work\FD\Output\\{0}\\", day_time)
    return ret_folder

def get_save_path():
    global sub_timedelta
    yesterday = date.today() - timedelta(sub_timedelta)
    save_folder = str.format("D:\Work\FD\Downloads\\{0}\\", yesterday)
    return save_folder

def get_suspicious_path():
    folder = str.format("D:\Work\FD\Suspicious\\")
    return folder

def get_json_path():
    global sub_timedelta
    yesterday = date.today() - timedelta(sub_timedelta)
    file_path = "D:\Work\FD\Json\\" + str(yesterday) + ".json"
    return file_path

def get_copy_path(file_name, lines):
    global sub_timedelta
    yesterday = date.today() - timedelta(sub_timedelta)
    file_path = str.format("D:\Work\FD\Suspicious\{0}-{1}-{2}", yesterday, lines, file_name)
    return file_path

def get_start_date():
    ret_date = date.today() - timedelta(sub_timedelta)
    pt_time  = time.strptime(str(ret_date), '%Y-%m-%d')
    str_time = time.strftime("%Y/%m/%d",pt_time)
    return str_time

def get_end_date():
    ret_date = date.today() - timedelta(sub_timedelta) + timedelta(1)
    pt_time  = time.strptime(str(ret_date), '%Y-%m-%d')
    str_time = time.strftime("%Y/%m/%d",pt_time)
    return str_time