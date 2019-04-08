# -*- coding: utf-8 -*-

import os
import requests
import json
import time
import random
import hashlib
import base64
import re

try:
    import urlparse   # Python 2
except ImportError:
    from urllib import parse as urlparse   # Python 3


# 注意, 向 APM 成员索要 Secret 并替换 "put-your-web-token-here"
WEB_TOKEN_SECRET = "SngWebApm123"

# 注意, 不是公共集群的产品需要修改访问的 HOST
#WEB_BASE_URL = "https://sngapm.qq.com/web/1/"
WEB_BASE_URL = "https://sngapm.qq.com/web/1/"

USER_NOBODY = "nobody"
USER_NAME = "api"
QAPM_WEB_TOKEN = "cWFwbXx8MTU3NjcyNjE5MTcyOTY0NDg3ZjFhOGE5MWJhNzIwZDA0ZTFkMWRhMDJiM2NlODVhYjU="
if not QAPM_WEB_TOKEN:
    raise RuntimeError("EXIT, EXIT, EXIT, not found environment variable: 'QAPM_WEB_TOKEN'")

class AuthToken(object):
    """
    token 格式:
            token:     10位unix时间戳+8位random整数+md5-value
            md5-value: md5(10位unix时间戳+8位random整数+secret)
    """
    def __init__(self, secret, expire_sec=None):
        self.expire_sec = expire_sec or 300
        self.secret = secret
        if not self.secret:
            raise RuntimeError("AuthToken.__init__(), not found secret ...")

    def gen_token(self, user_name=""):
        user_name = user_name or USER_NOBODY
        stamp = str(int(time.time()))
        rand = random.randint(10000000, 99999999)
        v = "%s||%s%8d%s" % (user_name, stamp, rand, self.secret)
        md5_value = hashlib.md5(v.encode('utf-8')).hexdigest()
        # print "stamp: %s, rand: %s, md5_value: %s" % (stamp, rand, md5_value)
        raw = "%s||%s%8d%s" % (user_name, stamp, rand, md5_value)
        return base64.b64encode(raw.encode('utf-8'))


class SngapmWebApiAction(object):
    WAREHOUSE_FILTER = "warehouse_filter"
    DOWNLOAD_FILE = "download_file"

    def __init__(self, action):
        self.action = action
        if action not in self.__dict__.values():
            raise ValueError("action(%s) not in: %s" % (action, self.__dict__.values()))

    @property
    def url(self):
        if self.action == self.WAREHOUSE_FILTER:
            return urlparse.urljoin(WEB_BASE_URL, "api/warehouseFilter/")
        elif self.action == self.DOWNLOAD_FILE:
            return urlparse.urljoin(WEB_BASE_URL, "api/downloadFile/")
        else:
            raise ValueError("not found action url of: %s" % self.action)

    def call(self, p_id, params=None):
        para = dict(p_id=p_id)
        if isinstance(params, dict):
            para.update(params)
        auth_token = AuthToken(secret=WEB_TOKEN_SECRET)

        ##print("SngapmWebApiAction.call, url: %s, para: %s" % (self.url, para))
        resp = requests.post(self.url, data=para, timeout=60, headers={"token": QAPM_WEB_TOKEN, "username": USER_NAME, "X-Forwarded-For": "127.0.0.1"})

        # 判断是否是文件下载
        filename = (re.findall("filename=(.+)", resp.headers.get("content-disposition", "")) or [""])[0]
        if filename:
            output_dir = params.get("real_output_dir", "./")
            print(output_dir)
            output_filename = params.get("output_filename", filename)
            output_path = os.path.join(output_dir, output_filename)
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            print("SngapmWebApiAction.call, write file: %s" % output_path)
            with open(output_path, "wb") as fd:
                for chunk in resp.iter_content(chunk_size=4*1024):
                    fd.write(chunk)
        else:
            try:
                d = json.loads(resp.text)
                print(d)
            except:
                raise RuntimeError("SngapmWebApiAction.call, resp is not json: %s" % str(resp.text))
            if d.get("status", None) != "ok":
                raise RuntimeError("SngapmWebApiAction.call, resp with error: %s" % d.get("data", "not get error msg ..."))
            return d.get("data", None)


class SngapmWebApi(object):
    def __init__(self):
        pass

    @staticmethod
    def call_action(action, p_id, params=None):
        """
        :param action: required, 操作名称, refer: class SngapmWebApiAction, string
        :param p_id: required, 产品 ID, sngapm web 页面参数可查看到 p_id, int
        :param params: 额外参数, dict
        :return:
        """
        act = SngapmWebApiAction(action=action)
        return act.call(p_id=p_id, params=params)

    def shortcut_download_warehouse_files(self, p_id, params=None, re_download=False):
        """
        :param p_id: required, 产品 ID, sngapm web 页面参数可查看到 p_id, int
        :param params: required, 额外参数, 详情如下, dict
            zone:        required, 表名, string
            output_dir:  optional, 下载文件的输出目录, default: "./", string
            time_range:  optional, 时间范围, 格式必须为: "2017/11/14 - 2017/11/19", default: None, string
            version:     optional, 选择特定版本, 模糊查询, 后台实现为 LIKE, default: None, string
            device:      optional, 选择特定机型, default: None, string
            is_vip:      optional, 选择是否Vip用户, True | False, default: None, string
            uin:         optional, 选择特定Uin的用户, default: None, string
            limit:       optional, 限制最大条数, default: 500, string
        :param re_download: optional, 文件存在时是否重新下载, default: False, bool
        :return:
        """
        records = self.call_action(action=SngapmWebApiAction.WAREHOUSE_FILTER, p_id=p_id, params=params)
        ##print("SngapmWebApi.shortcut_download_warehouse_files, get %s records with para: %s" % (len(records), params))
        for index, record in enumerate(records):
            try:
                print("[%d] SngapmWebApi.shortcut_download_warehouse_files, will download of (%s - %s): %s" % (index, record["version"], record["uin"], record))
                ##print("[%d] SngapmWebApi.shortcut_download_warehouse_files, will download with url: %s" % (index, record["apm_entrance_filepath"]))
                download_params = dict(
                    p_id=p_id,
                    file_path=record["apm_entrance_filepath"],
                    type="cos",
                    encryption_type="none",
                    # output_dir="./traces"
                )
                if record["apm_entrance_filepath"] is None:
                    print("[%d] SngapmWebApi.shortcut_download_warehouse_files, url is none, skip: %s" % (index, output_path))
                    continue

                download_params["output_filename"] = "%s.%s" % (record["apm_identify"][:8], record["apm_entrance_filepath"].split('/')[-1]+".zip")
                pt_time  = time.strptime(str(record["time_day"]), '%Y%m%d')
                str_time = time.strftime("%Y-%m-%d",pt_time)
                output_dir = "D:\\Work\\FD\\Downloads\\%s\\" % (str_time)
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)
                if params is not None:
                    download_params.update(params)
                download_params['real_output_dir'] = output_dir
                output_path = os.path.join(output_dir, download_params["output_filename"])
                if not re_download and os.path.exists(output_path):
                    print("[%d] SngapmWebApi.shortcut_download_warehouse_files, already exists, skip: %s" % (index, output_path))
                    continue

                record_dir = "D:\\Work\\FD\\Params\\%s\\" % (str_time)
                if not os.path.exists(record_dir):
                    os.mkdir(record_dir)
                record_path = os.path.join(record_dir, "%s.%s" % (record["apm_identify"][:8], record["apm_entrance_filepath"].split('/')[-1]+".txt"))
                f = open(record_path,'wb')
                f.write(json.dumps(record).encode("utf-8"))
                f.close()

                self.call_action(action=SngapmWebApiAction.DOWNLOAD_FILE, p_id=p_id, params=download_params)
                time.sleep(0.5)
            except Exception as e:
                print("[%d] SngapmWebApi.shortcut_download_warehouse_files, download failed, %s" % (index, e))

def gain_data_from_yun(st, et):
    range = ("%s - %s" % (st, et))
    api = SngapmWebApi()
    api.shortcut_download_warehouse_files(p_id=1, params=dict(
        output_dir="D:\\Work\\FD\\NewAPI\\Downloads\\",
        zone="fd_monitor",    # others zone: traces_log_high_cpu  traces_log_dead_lock
        time_range= range,
        # version="7.5.5.798",
        # device="R823T",
        # is_vip="True",
        # uin="276500572",
        limit="99000",    # 默认最多返回 500 条, 可选择更大值
    ))
    # api.shortcut_download_warehouse_files(p_id=2, params=dict(
    #     output_dir="./",
    #     zone="df_log",    # others zone: traces_log_high_cpu  traces_log_dead_lock
    #     time_range="2017/12/14 - 2017/12/15",
    #     version="7.3.5.2618_AR3DCylinderRecog_363082_12-11_22:12",
    #     uin="1828946168",
    #     # device="R823T",
    #     # is_vip="True",
    #     limit="1000",    # 默认最多返回 500 条, 可选择更大值
    # ))
