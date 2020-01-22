"""
哈哈
本模块用于处理把windows中的\r\n 替换成\n 或 \r
by vacon
"""
import os

SUFFIX_LIST = [".sh", ".py", ".go", ".cpp", ".upload", ".yml", ".json"]  # 没有过滤xml和html


def get_all_file(root_node):
    """
    通过递归的方式获取root_node下所有的文件名
    :param root_node:
    :return:
    """
    ab_root = os.path.abspath(root_node)
    all_path_record = []
    next_level_paths = os.listdir(ab_root)
    next_level_abs_paths = [os.path.join(ab_root, filename) for filename in next_level_paths]
    # print(next_level_paths)
    # 空文件夹直接返回[]
    if not next_level_abs_paths:
        return []
    for tmp_path in next_level_abs_paths:
        # print("--", tmp_path)
        # 文件，直接添加
        if os.path.isfile(tmp_path):
            all_path_record.append(tmp_path)
        # 非文件，递归获取
        else:
            tmp_file_path = get_all_file(tmp_path)
            all_path_record += tmp_file_path
    return all_path_record


def get_all_dir(root_node):
    """
    通过递归的方式获取root_node下所有的路径
    :param root_node: 根目录
    :return:
    """
    ab_root = os.path.abspath(root_node)
    all_path_record = []
    next_level_paths = os.listdir(ab_root)
    next_level_abs_paths = [os.path.join(ab_root, filename) for filename in next_level_paths]
    # 空文件夹直接返回[]
    if not next_level_abs_paths:
        return []
    for tmp_path in next_level_abs_paths:
        if os.path.isdir(tmp_path):
            all_path_record.append(tmp_path)
            tmp_dir_path = get_all_dir(tmp_path)
            all_path_record += tmp_dir_path
        else:
            continue
    return all_path_record


def filter_file(file, filter_suffix_list):
    """
    过滤方式
    :param file: 文件路径名称
    :param filter_suffix_list: 如[".sh", ".py"]
    :return:
    """
    isfile = os.path.isfile(file)
    res = False
    for tmp_suffix in filter_suffix_list:
        res = res or file.endswith(tmp_suffix)
    return isfile and res


def process_all_file(file_dir, mode="linux"):
    """
    把文件从windows格式转换为linux格式或mac格式
    :param file_dir:
    :param mode:
        mac   windows to mac
        linux windows to linux
    :return:
    """
    abs_path = os.path.abspath(file_dir)
    print("处理的根目录是：", abs_path)
    window_crlf = "\r\n"

    if mode == "linux":
        to_crlf = "\n"
    else:
        to_crlf = "\r"

    # 获取所有.py .sh 的文件的路径
    all_files = get_all_file(abs_path)
    all_files_filter = [file_name for file_name in all_files if filter_file(file_name, SUFFIX_LIST)]
    print(all_files_filter)

    # debug
    # all_file_path = [r"D:\pyProj\qci_sp-master\process_crlf.py"]

    for tmp_file in all_files_filter:
        print("--", tmp_file)
        with open(tmp_file, encoding="utf-8", mode="r+") as pf_w:
            all_lines = pf_w.readlines()
            # print(all_lines)
            [line.replace(window_crlf, to_crlf) for line in all_lines if line.endswith(window_crlf)]
            # print(all_lines)
            pf_w.seek(0)
            pf_w.writelines(all_lines)


if __name__ == '__main__':
    process_all_file(r".")
