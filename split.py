import binascii
import re
import numpy as np
from PIL import Image
import io
import cv2
from utils import *

#######################################################
start_ptrn = 'ffd8'
end_ptrn = 'ffd9'
save_path_narrow = 'outputs/narrow'
save_path_wide = 'outputs/wide'
#######################################################

# 1. Create save directories
exists_or_mkdir(save_path_narrow)
exists_or_mkdir(save_path_wide)

# 2. Split!
_, filepaths, num = load_file_list('inputs')
if num == 1:
    filepaths = np.expand_dims(filepaths, 0)

for filepath in filepaths:
    # a. open image
    filename = os.path.basename(filepath).split('.')[0]
    with open(filepath, 'rb') as f:
        data = f.read()
    f.close()
    data = binascii.hexlify(data).decode('utf-8')

    # b. split images
    images = []
    end_idx_ = 0
    while True:
        image, start_idx, end_idx_ = get_start_end_idx(data, start_ptrn, end_ptrn, end_idx_)
        if image != -1:
            images.append(image)
        else:
            break;

    # c. save images
    print('number of hidden images: ', len(images))
    for i in np.arange(1, len(images)):
        image = binascii.unhexlify(images[i].encode())
        f = open('{}.jpg'.format(filename), 'wb')
        f.write(image)
        f.close()
        image = cv2.imread('{}.jpg'.format(filename), cv2.IMREAD_COLOR)

        if i == 1:
            cv2.imwrite('{}/{}.png'.format(save_path_narrow, filename), image)
        else:
            cv2.imwrite('{}/{}.png'.format(save_path_wide, filename), image)

        os.remove('{}.jpg'.format(filename))
