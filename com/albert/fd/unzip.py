import zipfile
from os.path import isfile, join, isdir
from os import listdir
import os
from com.albert.fd.visit import get_save_path

def iterate_zip(folder):
     for f in listdir(folder):
        absolute_path = str.format("{0}\\{1}", folder, f)
        if isdir(absolute_path):
            iterate_zip(absolute_path)
        elif zipfile.is_zipfile(absolute_path):
            print(str.format("detect {0}", absolute_path))
            zf = zipfile.ZipFile(absolute_path, 'r')
            extract_file_path = str(zf.filename)
            extract_file_path = extract_file_path[0:len(extract_file_path) - 4]
            zf.extractall(extract_file_path)
            zf.close()
            ## delete zip file
            if os.path.exists(absolute_path) :
                os.remove(absolute_path)
            ## iterate folder
            iterate_zip(extract_file_path)
        elif not absolute_path.endswith('.txt') and not absolute_path.endswith('.socket'):
            print(str.format("unknown file {0}", absolute_path))

def start_unzip():
    save_folder = get_save_path()
    print(str.format("start_unzip {0}", save_folder))
    if not os.path.exists(save_folder):
        print(str.format("unable to unzip {0} because no file", save_folder))
        return
    iterate_zip(save_folder)