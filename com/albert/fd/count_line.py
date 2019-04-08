from os.path import isfile, join, isdir
from os import listdir
from com.albert.fd.visit import get_save_path, get_copy_path, get_suspicious_path
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
                    last_line = line
                    if str(line).find(str(fd_name)) >= 0:
                        count = count + 1
                txt_file.close()
                if count > 2 and last_line.find('debug:0') >= 0:
                    print(str.format("find {0} has {1} ", absolute_path, count))

def find_fd(fd_name):
    save_folder = get_save_path()
    iterate_find(save_folder, fd_name)

class res_obj:
    res_str = ''
    res_cnt = 0

    def __init__(self, str, cnt):
        self.res_str = str
        self.res_cnt = cnt

    def __lt__(self, other):
        return self.res_cnt > other.res_cnt

class tree_node:
    node_id = 0
    str = ''
    cnt = 0
    node_list = None
    level = 0

    def __init__(self, i, s):
        self.node_id = i
        self.str = s
        self.cnt = 1
        self.node_list = []

    def add_one(self):
        self.cnt = self.cnt + 1

    def find_char_at_child(self, c):
        for child in self.node_list:
            if child.str == c:
                return child

        return None

    def add_child(self, child):
        self.node_list.append(child)

    def traverse(self, cur_str, res_list):
        if self.node_id == 0:
            new_str = cur_str
        else:
            new_str = cur_str + self.str

        if len(self.node_list) == 0:
            if self.cnt > 20:
                res_list.append(res_obj(new_str, self.cnt))
                return True
            else:
                return False

        if self.level > 100:
            return False

        handle = False
        for child in self.node_list:
            if child.traverse(new_str, res_list) :
                handle = True

        if not handle:
            if self.level > 4 and self.cnt > 20:
                res_list.append(res_obj(new_str, self.cnt))
                return True
            else:
                return False

        return True

class stats_tree:
    root_node = tree_node(0, '&')
    cur_count = 0
    res_list = None

    def __init__(self):
        self.cur_count = 0
        self.root_node = tree_node(0, '&')
        self.root_node.level = 0
        self.cur_count = self.cur_count + 1
        self.res_list = []

    def add_to_tree(self, str):
        ## add to tree
        pre_node = self.root_node
        for one_ch in str:
            ret_node = pre_node.find_char_at_child(one_ch)
            if ret_node == None:
                new_node = tree_node(self.cur_count, one_ch)
                new_node.level = pre_node.level + 1
                self.cur_count = self.cur_count + 1
                pre_node.add_child(new_node)
                pre_node = new_node
            else:
                ret_node.add_one()
                pre_node = ret_node

    def traverse_tree(self):
        self.root_node.traverse('', self.res_list)
        self.res_list.sort()
        size = min(len(self.res_list), 10)
        for i in range(0, size):
            print(str.format("{0} : {1}", self.res_list[i].res_str, self.res_list[i].res_cnt))

    def get_traverse_data(self):
        ret_map = {}
        self.root_node.traverse('', self.res_list)
        self.res_list.sort()
        size = min(len(self.res_list), 10)
        for i in range(0, size):
            ret_map[self.res_list[i].res_str] = self.res_list[i].res_cnt
        return ret_map

def count_same_demo():
    tree = stats_tree()
    tree.add_to_tree("abcd")
    tree.add_to_tree("abc")
    tree.add_to_tree("ab")
    tree.add_to_tree("acd")
    tree.add_to_tree("bc")
    tree.add_to_tree("bd")
    tree.add_to_tree("acd")
    tree.add_to_tree("bde")
    tree.add_to_tree("bcd")
    tree.traverse_tree()


def iterate_count_same_fd(folder):
    for f in listdir(folder):
        absolute_path = str.format("{0}\\{1}", folder, f)
        if isdir(absolute_path):
           iterate_count_same_fd(absolute_path)
        elif isfile(absolute_path):
            if absolute_path.endswith('.txt'):
                lines = len(open(absolute_path,'rU', encoding='utf-8').readlines())
                if lines > 800:
                    print(str.format("{0} has {1} lines", absolute_path, lines))
                    txt_file = open(absolute_path, "r", encoding='utf-8')
                    tree = stats_tree()
                    last_line = ""
                    for line in txt_file:
                        line = line.strip('\n')
                        tree.add_to_tree(line)
                        last_line = line
                    tree.traverse_tree()
                    print('\n' + last_line)

                    suspicious = input(str.format("Is it suspicious?(y/n)"))
                    if suspicious == 'y':
                        dst_path = get_copy_path(str(f), lines)
                        print("dest path ", dst_path)
                        shutil.copyfile(absolute_path, dst_path)

                    txt_file.close()
                else:
                    print(str.format("{0} has {1} lines", absolute_path, lines))

i_list = {1, 2, 3, 4, 5, 6}
line_num_list = {1:500, 2:600, 3:700, 4:800, 5:900, 6:0}
res_count = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
output_list = {1:'2-500', 2:'501-600', 3:'601-700', 4:'701-800', 5:'801-900', 6:'900+', 7:'0'}

def iterate_count_distribution(folder):
    for f in listdir(folder):
        absolute_path = str.format("{0}\\{1}", folder, f)
        if isdir(absolute_path):
           iterate_count_distribution(absolute_path)
        elif isfile(absolute_path):
            if absolute_path.endswith('.txt'):
                lines = len(open(absolute_path,'rU', encoding='utf-8').readlines())
                handle = False
                # if lines < 10:
                #     print("%s has %s" % (absolute_path, lines))
                if int(lines) == 0 or int(lines) == 1:
                    res_count[7] = int(res_count[7]) + 1
                else:
                    for i in i_list:
                        line_num = int(line_num_list[i])
                        if int(lines) < line_num:
                            res_count[i] = int(res_count[i]) + 1
                            handle = True
                            break
                    if not handle:
                        res_count[6] = int(res_count[6]) + 1


def count_same_fd():
    save_folder = get_save_path()
    iterate_count_same_fd(save_folder)

def count_suspicious_fd():
    iterate_count_same_fd(get_suspicious_path())

def count_distribution():
    for key in res_count:
        res_count[key] = int(0)
    iterate_count_distribution(get_save_path())
    str_print = "distribution is ["
    for key in res_count:
        str_print += "\'%s\' : %s, " % (output_list[key], res_count[key])
    str_print += "]"
    print(str_print)