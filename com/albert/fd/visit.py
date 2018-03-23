import webbrowser
from datetime import date, timedelta

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


def get_save_path():
    global sub_timedelta
    yesterday = date.today() - timedelta(sub_timedelta)
    save_folder = str.format("D:\Work\FD\Downloads\\{0}\\", yesterday)
    return save_folder

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