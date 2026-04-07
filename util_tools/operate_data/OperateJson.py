import json
import os.path

from config.setting import FILE_PATH


def operate_json(filename, is_remove_desc=True):
    filepath = os.path.join(FILE_PATH.get("data"), filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
        data_list = []
        for data in original_data:
            if is_remove_desc:
                data_tuple = tuple(data.values())[1:]
            else:
                data_tuple = tuple(data.values())
            data_list.append(data_tuple)

    return data_list


if __name__ == '__main__':
    print(operate_json("login.json",is_remove_desc=False))
    # print(operate_json("register_success.json"))
    print(operate_json("register_fail.json",is_remove_desc=False))
    print(operate_json("different_settle_user.json"))
