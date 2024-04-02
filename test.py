def slide(key_list):
    tree_dict = {}
    for key in key_list:
        split_list = key.split('-', 1)
        if split_list[0] not in tree_dict:
            tree_dict[split_list[0]] = []
            if len(split_list) > 1:
                tree_dict[split_list[0]].append(split_list[1])
            else:
                tree_dict[split_list[0]] = 'all'
        else:
            if isinstance(tree_dict[split_list[0]], list):
                if len(split_list) > 1:
                    tree_dict[split_list[0]].append(split_list[1])
                else:
                    tree_dict[split_list[0]] = 'all'

    for k, v in tree_dict.items():
        if isinstance(v, list):
            tree_dict[k] = slide(v)
    return tree_dict

key_l = ['0-1-1-0', '0-1-2-1', '0-2-0-1']
print(slide(key_l))
