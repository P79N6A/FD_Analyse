import json
import requests
import os
from com.albert.fd.visit import get_save_path, get_json_path

def start_download():
    file_path = get_json_path()
    file = open(file_path, "r")
    load_json = json.load(file)
    file.close()

    download_url_prefix = "http://10.185.18.32/"
    save_folder = get_save_path()
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    for item in load_json:
        dump_file = item['filepath']
        id = item['id']
        save_file_path = save_folder + str.format("{0}.zip", id)
        print(str.format("start download {0}", save_file_path))
        if os.path.exists(save_file_path) :
            os.remove(save_file_path)
        ##download
        url = download_url_prefix + str(dump_file)
        f = requests.get(url)
        with open(save_file_path, "wb") as fs:
            fs.write(f.content)
        print(str.format("end download {0}", save_file_path))
        # ## unzip
        # if zipfile.is_zipfile(save_file_path):
        #     zf = zipfile.ZipFile(save_file_path, 'r')
        #     zf.extractall(extract_file_path)
        #     zf.close()
        #     print("zip end")
        # else:
        #     print("not zip")
        # ## delete zip file
        # if os.path.exists(save_file_path) :
        #     os.remove(save_file_path)