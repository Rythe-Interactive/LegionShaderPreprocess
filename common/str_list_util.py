def str_list_append(str_list, to_append):
    return ','.join(list(filter(None, str_list.split(',') + [to_append])))


def dict_str_list_append(d, key, to_append):
    d[key] = str_list_append(d.setdefault(key, ''), to_append)


def dict_str_list_append_list(d, key, list_to_append):
    dict_str_list_append(d, key, ','.join(list_to_append))
