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

# Create save directories
exists_or_mkdir(save_path_narrow)
exists_or_mkdir(save_path_wide)

_, filepaths, _ = load_file_list('inputs')
for filepath in filepaths:
    file_name = os.path.basename(filepath).split('.')[0]
    with open(filepath, 'rb') as f:
        data = f.read()
    f.close()

    data = binascii.hexlify(data).decode('utf-8')

    images = []
    end_idx_ = 0
    while True:
        image, start_idx, end_idx_ = get_start_end_idx(data, start_ptrn, end_ptrn, end_idx_)
        if image != -1:
            images.append(image)
        else:
            break;

    for i in np.arange(len(images)):
        image = binascii.unhexlify(images[i].encode())
        f = open('output{}.jpg'.format(i), 'wb')
        f.write(image)
        f.close()
        image = cv2.imread('output{}.jpg'.format(i), cv2.IMREAD_COLOR)
        print(image.shape)
        cv2.imwrite('output{}.png'.format(i), image)
