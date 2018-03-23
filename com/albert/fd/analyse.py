from com.albert.fd.download import start_download
from com.albert.fd.unzip import start_unzip
from com.albert.fd.count_line import count, find_fd
from com.albert.fd.visit import visit, set_timedelta

while 1:
    cmd = input('Input cmd:')
    if cmd == 'exit':
        break;
    elif cmd == '0':
        timedelta = input("Input timedelta:")
        set_timedelta(timedelta)
    elif cmd == '1':
        timedelta = input("Input timedelta:")
        visit(timedelta)
    elif cmd == '2':
        start_download()
    elif cmd == '3':
        start_unzip()
    elif cmd == '4':
        print_all = input("need print all?")
        count(print_all)
    elif cmd == '5':
        fd_name = input("type in fd name:")
        find_fd(fd_name)