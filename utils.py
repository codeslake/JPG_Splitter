import os
import numpy as np

def load_file_list(root_path, child_path = None):

    folder_paths = []
    filenames_pure = []
    filenames_structured = []
    num_files = 0
    for root, dirnames, filenames in os.walk(root_path):
        if len(dirnames) == 0:
            if root[0] == '.':
                continue
            if child_path is not None and child_path not in root: 
                continue
            folder_paths.append(root)
            filenames_pure = []
            for i in np.arange(len(filenames)):
                if filenames[i][0] != '.':
                    filenames_pure.append(os.path.join(root, filenames[i]))
            filenames_structured.append(np.array(sorted(filenames_pure)))
            num_files += len(filenames_pure)

    folder_paths = np.array(folder_paths)
    filenames_structured = np.array(filenames_structured)

    sort_idx = np.argsort(folder_paths)
    folder_paths = folder_paths[sort_idx]
    filenames_structured = filenames_structured[sort_idx]

    return folder_paths, np.squeeze(filenames_structured), num_files

def exists_or_mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    else:
        return True


def get_start_end_idx_v2(data, start_ptrn, end_ptrn, end_idx):

    start_idx = 1
    start_idx_temp = end_idx
    while start_idx % 2 != 0:
        start_idx = data.find(start_ptrn, start_idx_temp)
        start_idx_temp += 1
        if start_idx == -1:
            return -1, None, None

    end_idx = 1
    end_idx_temp = start_idx + 1
    while end_idx % 2 != 0:
        end_idx = data.find(start_ptrn, end_idx_temp)
        end_idx_temp = end_idx + 1
        if end_idx == -1:
            end_idx = len(data)
            break;

    data_temp = data[start_idx:end_idx]

    return data_temp, start_idx, end_idx

def get_start_end_idx(data, start_ptrn, end_ptrn, end_idx):

    start_idx = 1
    start_idx_temp = end_idx
    while start_idx % 2 != 0:
        start_idx = data.find(start_ptrn, start_idx_temp)
        start_idx_temp += 1
        if start_idx == -1:
            return -1, None, None

    end_idx = 1
    end_idx_temp = start_idx + 1
    while end_idx % 2 != 0:
        end_idx = data.find(end_ptrn, end_idx_temp)
        end_idx_temp = end_idx + 1
        if end_idx == -1:
            break;

    data_temp = data[start_idx:end_idx+4]

    return data_temp, start_idx, end_idx
