# REFERENCE
#  - 参考np的分块方法numpy.array_split，20 = 4*2 + 3*4 [6 chunks]

# QUESTION
#  - only can split list or ???

# TODO
#  - 优化变量和方法(命名/范围)
#  - 优化重复低效操作
#  - 优化错误处理
#  - 总结一下

# ATTENTION
#  - ****** [(slice_begin, slice_end), ...] > list[x:y] > [x, y) > so index slice_end need +1 ******

import os, time, re, inspect


def split_number_to_x1x2_plus_y1y2(number, chunk):
    if type(number) != int:
        return "number not int"
    if type(chunk) != int:
        return "chunk not int"
    if number < 2:
        return "number < 2"
    if chunk < 2:
        return "chunk < 2"
    result = []
    offset = 0
    if number // chunk == number / chunk:
        return (chunk, number // chunk)
    else:
        flag = True
        temp = {}
        while flag:
            offset += 1
            x_num = number // chunk + offset
            for i in range(1, chunk):
                x_chunk = i
                y_chunk = chunk - i
                if number - (x_chunk * x_num) <= 0:
                    flag = False
                    break
                if ((number - (x_num * x_chunk)) //
                        y_chunk) == ((number - (x_num * x_chunk)) / y_chunk):
                    result.append((x_chunk, x_num, y_chunk,
                                   (number - (x_num * x_chunk)) // y_chunk))
                else:
                    continue
                if i == chunk - 1:
                    flag = False
    return result


def split_list_by_chunk_choice(total, chunk):
    if type(total) != int:
        return "total not int"
    if type(chunk) != int:
        return "chunk not int"
    if total < 2:
        return "total < 2"
    if chunk < 2:
        return "chunk < 2"
    split_ways = split_number_to_x1x2_plus_y1y2(total, chunk)
    result = {}
    if not split_ways:
        return "cant split by this chunk"
    if type(split_ways) == tuple:
        result["x_y_chunk"] = split_ways[0]
        result["x_y_num"] = split_ways[1]
    else:
        diffs = []
        for index, item in enumerate(split_ways):
            if item[1] - item[3] >= 0:
                temp = {}
                temp["result_index"] = index
                temp["diff"] = item[1] - item[3]
                diffs.append(temp)
            else:
                continue
        diffs = sorted(diffs, key=lambda x: x["diff"], reverse=False)
        best_way = split_ways[diffs[0]["result_index"]]
        result["x_chunk"] = best_way[0]
        result["x_num"] = best_way[1]
        result["y_chunk"] = best_way[2]
        result["y_num"] = best_way[3]
    return result


def SLOW_split_number_to_x1x2_plus_y1y2(number, chunk):
    if type(number) != int:
        return "number not int"
    if type(chunk) != int:
        return "chunk not int"
    if number < 2:
        return "number < 2"
    if chunk < 2:
        return "chunk < 2"
    # chunk == x_chunk + y_chunk
    # number == x_chunk * x_num + y_chunk * y_num
    # better > min(x_num - y_num)
    # -------------------------
    # eg: 20 = 2 * [4] + 4 * [3]
    # ----------
    # [0 1 2 3]
    # [4 5 6 7]
    # ----------
    # [8  9 10]
    # [11 12 13]
    # [14 15 16]
    # [17 18 19]
    # -------------------------
    result = []
    for i in range(1, chunk):
        x_chunk = i
        y_chunk = chunk - x_chunk
        for j in range(1, number - y_chunk + 1):
            x_num = j
            if (number -
                (x_chunk * x_num)) // y_chunk != (number -
                                                  (x_chunk * x_num)) / y_chunk:
                continue
            if number - (x_chunk * x_num) <= 0:
                continue
            y_num = (number - (x_chunk * x_num)) // y_chunk
            print("%d == %d * [%d] + %d * [%d] \n" %
                  (number, x_chunk, x_num, y_chunk, y_num))
            temp = (x_chunk, x_num, y_chunk, y_num)
            result.append(temp)
    return result


def SLOW_split_list_by_chunk_choice(total, chunk):
    if type(total) != int:
        return "total not int"
    if type(chunk) != int:
        return "chunk not int"
    if total < 2:
        return "total < 2"
    if chunk < 2:
        return "chunk < 2"
    split_ways = SLOW_split_number_to_x1x2_plus_y1y2(total, chunk)
    diffs = []
    for index, item in enumerate(split_ways):
        if item[1] - item[3] >= 0:
            temp = {}
            temp["result_index"] = index
            temp["diff"] = item[1] - item[3]
            diffs.append(temp)
        else:
            continue
    best_way = split_ways[sorted(diffs, key=lambda x: x["diff"],
                                 reverse=False)[0]["result_index"]]
    result = {}
    if best_way[1] == best_way[3]:
        result["x_y_chunk"] = best_way[0] + best_way[2]
        result["x_y_num"] = best_way[1]
    else:
        result["x_chunk"] = best_way[0]
        result["x_num"] = best_way[1]
        result["y_chunk"] = best_way[2]
        result["y_num"] = best_way[3]
    return result


def split_list_by_number_return_list(source_list, split_num):
    if type(source_list) is not list:
        return "collection is not list"  # TODO return -> exception
    if len(source_list) == 0:
        return "null list"
    if type(split_num) is not int:
        return "split_num is not int"
    if split_num <= 0:
        return "split num <= 0"
    if split_num > len(source_list):
        return "split num > len(list)"
    result = []
    for slice_begin, slice_end in split_list_by_number_return_slice_index(
            source_list, split_num):
        result.append(source_list[slice_begin:slice_end])
    return result


def split_list_by_number_return_slice_index(source_list, split_num):
    if type(source_list) is not list:
        return "collection is not list"  # TODO return -> exception
    if len(source_list) == 0:
        return "null list"
    if type(split_num) is not int:
        return "split_num is not int"
    if split_num <= 0:
        return "split num <= 0"
    if split_num > len(source_list):
        return "split num > len(list)"
    result = []
    len_total = len(source_list)
    len_split_num = split_num
    len_chunk = 1
    div_float = len_total / len_split_num
    div_int = len_total // len_split_num
    len_remain = -1
    if div_int == div_float:
        len_chunk = div_int
    elif div_int < div_float:
        len_chunk = div_int + 1
        len_remain = len_total - div_int * len_split_num
    else:
        return "error divide"
    if len_remain == -1:
        for i in range(len_chunk):
            temp = (i * len_split_num, (i + 1) * len_split_num)
            result.append(temp)
    else:
        for i in range(len_chunk):
            if i != len_chunk - 1:
                temp = (i * len_split_num, (i + 1) * len_split_num)
                result.append(temp)
            else:
                if len_remain == 1:
                    temp = (i * len_split_num, len_total)
                    result.append(temp)
                else:
                    temp = (i * len_split_num, len_total)
                    result.append(temp)
    return result


def split_list_by_chunk_return_list(source_list, chunk):
    if type(source_list) is not list:
        return "collection is not list"  # TODO return -> exception
    if not source_list:
        return "null list"
    if type(chunk) is not int:
        return "chunk is not int"
    if chunk < 2:
        return "chunk < 2"
    if chunk > len(source_list):
        return "chunk > len(list)"
    slice_indices = split_list_by_chunk_return_slice_index(source_list, chunk)
    result = []
    for slice_begin, slice_end in slice_indices:
        result.append(source_list[slice_begin:slice_end])
    return result


def split_list_by_chunk_return_slice_index(source_list, chunk):
    if type(source_list) is not list:
        return "collection is not list"  # TODO return -> exception
    if not source_list:
        return "null list"
    if type(chunk) is not int:
        return "chunk is not int"
    if chunk < 2:
        return "chunk < 2"
    if chunk > len(source_list):
        return "chunk > len(list)"
    result = []
    split_way = split_list_by_chunk_choice(len(source_list), chunk)
    if not split_way:
        return "cant split by this chunk"
    else:
        if len(split_way) == 2:
            x_y_chunk = split_way["x_y_chunk"]
            x_y_num = split_way["x_y_num"]
            for i in range(x_y_chunk):
                result.append((i * x_y_num, (i + 1) * x_y_num))
        else:
            x_chunk = split_way["x_chunk"]
            x_num = split_way["x_num"]
            y_chunk = split_way["y_chunk"]
            y_num = split_way["y_num"]
            y_begin = x_chunk * x_num
            for i in range(x_chunk):
                result.append((i * x_num, (i + 1) * x_num))
            for i in range(y_chunk):
                result.append((i * y_num + y_begin, (i + 1) * y_num + y_begin))
    return result


def split_list_by_number(source_list, number):
    return split_list_by_number_return_list(source_list, number)


def split_list_by_chunk(source_list, chunk):
    return split_list_by_chunk_return_list(source_list, chunk)


def peek_file(path, line_num):
    with open(path, "r", encoding="utf-8") as f:
        for _ in range(line_num):
            print(f.readline())


def listdir(path):
    result = {}
    result["name"] = []
    result["path"] = []
    result["abs"] = []
    for f_d in os.listdir(path):
        result["name"].append(f_d)
        if "\\" in path:
            if path.endswith("\\"):
                result["path"].append(path + f_d)
                result["abs"].append(os.path.abspath(path + f_d))
            else:
                result["path"].append(path + "\\" + f_d)
                result["abs"].append(os.path.abspath(path + "\\" + f_d))
        if "/" in path:
            if path.endswith("/"):
                result["path"].append(path + f_d)
                result["abs"].append(os.path.abspath(path + f_d))
            else:
                result["path"].append(path + "/" + f_d)
                result["abs"].append(os.path.abspath(path + "/" + f_d))
    return result


def print_list(list_):
    print(*list_, sep="\n")


def current_time():
    return time.strftime("%Y%m%d_%H%M", time.localtime(time.time()))


def print_var(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    varname = [
        var_name for var_name, var_val in callers_local_vars if var_val is var
    ][0]
    print(f"{varname}: {var}")
