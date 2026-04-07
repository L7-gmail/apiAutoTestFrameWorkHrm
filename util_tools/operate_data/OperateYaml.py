import os
import yaml
from config.setting import FILE_PATH
from util_tools.log_util.RecordLog import logs


def operate_yaml(filename):
    try:
        data_list_tuple = []
        file = os.path.join(FILE_PATH.get("data"), filename)
        with open(file, 'r', encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        for data_str in data:
            data_list_tuple.append(tuple(data_str.split(',')))
        return data_list_tuple
    except Exception as e:
        logs.info(f"读取yaml文件测试数据异常，异常为：{e}")


if __name__ == '__main__':
    print(operate_yaml("address_info.yaml"))
    print(operate_yaml("settle_info.yaml"))
