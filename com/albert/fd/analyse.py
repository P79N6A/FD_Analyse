from com.albert.fd.download import start_download
from com.albert.fd.unzip import start_unzip
from com.albert.fd.count_line import count, find_fd, count_same_fd, count_same_demo, count_suspicious_fd, count_distribution
from com.albert.fd.visit import visit, set_timedelta, get_start_date, get_end_date
from com.albert.fd.custom_analyse import find_report_by_uin, find_report_by_uins, find_report_by_uins_new
from com.albert.fd.sngapm_api import gain_data_from_yun
from com.albert.fd.socket_stat import socket_stat
from com.albert.fd.Report import generate_report
import os

##cur_time = input("Need data of how many days ago?")
##set_timedelta(cur_time)
while 1:
    cmd = input('Input cmd:')
    if cmd == 'exit':
        break
    elif cmd == '0':
        timedelta = input("Input timedelta:")
        set_timedelta(timedelta)
    elif cmd == '1':
        st = get_start_date()
        et = get_end_date()
        gain_data_from_yun(st, et)
        start_unzip()

        #os.system('shutdown -s -t 120')    #关机

    elif cmd == '99':
        start_unzip()
    elif cmd == '2':
        count_same_fd()
    elif cmd == '3':
        generate_report()
    elif cmd == '4':
        fd_name = input("type in fd name:")
        find_fd(fd_name)
        ##print_all = input("need print all?")
        ##count(print_all)
        ##socket_stat()
    elif cmd == '5':
        find_report_by_uins()
    elif cmd == '6':
        count_suspicious_fd()
    elif cmd == '7':
        count_distribution()
    elif cmd == '8':
        uin = input("input uin to find:")
        date_time = input("input date time:")
        find_report_by_uin(uin, date_time)
    elif cmd == '9':
        date_time = input("input date time:")
        find_report_by_uins_new(date_time)


