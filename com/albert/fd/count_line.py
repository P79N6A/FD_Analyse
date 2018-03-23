from os.path import isfile, join, isdir
from os import listdir
from com.albert.fd.visit import get_save_path, get_copy_path
import shutil

print_all_flag = False

def iterate_files(folder):
    for f in listdir(folder):
        absolute_path = str.format("{0}\\{1}", folder, f)
        if isdir(absolute_path):
           iterate_files(absolute_path)
        elif isfile(absolute_path):
            if absolute_path.endswith('.txt'):
                txt_file = open(absolute_path, "r", encoding='utf-8')
                lines = len(txt_file.readlines())
                if lines > 600:
                    need_copy = input(str.format("{0} fd count is {1}.\nneed copy?(y/n)", txt_file.name, lines))
                    if need_copy == 'y':
                        dst_path = get_copy_path(str(f), lines)
                        print("dest path ", dst_path)
                        shutil.copyfile(absolute_path, dst_path)
                elif print_all_flag == 'yes':
                    print(lines)
                txt_file.close()

def count(print_all):
    global print_all_flag
    print_all_flag = print_all
    save_folder = get_save_path()
    iterate_files(save_folder)

def iterate_find(folder, fd_name):
    for f in listdir(folder):
        absolute_path = str.format("{0}\\{1}", folder, f)
        if isdir(absolute_path):
           iterate_find(absolute_path, fd_name)
        elif isfile(absolute_path):
            if absolute_path.endswith('.txt'):
                txt_file = open(absolute_path, "r", encoding='utf-8')
                count = 0
                for line in txt_file:
                    if str(line).find(str(fd_name)) >= 0:
                        count = count + 1
                txt_file.close()
                if count > 1:
                    print(str.format("find {0} has {1} ", absolute_path, count))

def find_fd(fd_name):
    save_folder = get_save_path()
    iterate_find(save_folder, fd_name)