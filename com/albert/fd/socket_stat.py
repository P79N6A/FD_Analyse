__author__ = 'alberthe'

from os.path import isfile, join, isdir, exists
from os import listdir
from com.albert.fd.visit import get_save_path, get_copy_path, get_suspicious_path
import shutil

def iterate_socket_stat(folder):
    if not exists(folder):
        return

    for f in listdir(folder):
        absolute_path = str.format("{0}\\{1}", folder, f)
        if isdir(absolute_path):
           iterate_socket_stat(absolute_path)
        elif isfile(absolute_path):
            if absolute_path.endswith('.txt'):
                end = f.find('.txt')
                socket_file = f[:end] + '.socket'
                absolute_socket_file = str.format("{0}\\{1}", folder, socket_file)
                if exists(absolute_socket_file):
                    txt_file = open(absolute_path, "r", encoding='utf-8')
                    count = 0
                    inode_list = []
                    for line in txt_file:
                        if str(line).find('socket') >= 0:
                            count = count + 1
                            start = str(line).find('[')
                            end = str(line).find(']')
                            inode = str(line)[start + 1:end]
                            inode_list.append(inode)

                    print("socket count:", count)
                    if count > 50:
                        need = input(str.format("{0} has {1} sockets .\nneed analyse?(y/n)", txt_file.name, count))
                        if need == 'y':
                            for i in inode_list:
                                soc_file = open(absolute_socket_file, "r", encoding='utf-8')
                                for sl in soc_file:
                                    if sl.find(i) >= 0:
                                        print("inode: ", i, sl)
                                soc_file.close()

                    txt_file.close()

def socket_stat():
    save_folder = get_save_path()
    iterate_socket_stat(save_folder)