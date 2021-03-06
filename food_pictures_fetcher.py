import os
import json
import time
from random import random
from utils import get_html, download_and_save_image, get_soup, resize_picture


height, width = 256, 256
N_MAX_IMAGES = 50


for folder_name in os.listdir('_data/ingredients'):

    print('Looking for pictures of ', folder_name)
    query = folder_name.split()
    query = '+'.join(query)
    url = 'https://www.google.co.in/search?q=' + query + '&source=lnms&tbm=isch'
    print(url)

    # add the directory for your image here
    ROOT_DIRECTORY = '_data_pictures'
    soup = get_soup(url)

    actual_images = []# contains the link for Large original images, type of image
    for a in soup.find_all("div", {"class":"rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        actual_images.append((link, Type))

    print('There is a total of ' , len(actual_images), 'images')

    query_directory = os.path.join(ROOT_DIRECTORY, folder_name)
    if not os.path.exists(query_directory):
        os.makedirs(query_directory)

    for i, (img_url, Type) in enumerate(actual_images):

        if i > N_MAX_IMAGES: break
        picture_path = os.path.join(query_directory, '{}_{}.jpg'.format(folder_name, i))
        if os.path.exists(picture_path):
            continue
        print('picture_path : ', picture_path)

        success_save = download_and_save_image(img_url, picture_path)
        success_resize = resize_picture(picture_path, height, width)

        if success_save and success_resize:
            sleep_time = 5 + 5 * random()
            print('Sleeping {}'.format(sleep_time))
            time.sleep(sleep_time)
