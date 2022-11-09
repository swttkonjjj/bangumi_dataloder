from requests import Session, exceptions
from requests.adapters import HTTPAdapter
from config import LOG_FOLDER
import time
import os
import logging
import filetype
from tqdm import tqdm
import re
# # from video import Video
# from data import insert_data
# from concurrent.futures import ThreadPoolExecutor

api_request = Session()
api_request.mount('http://', HTTPAdapter(max_retries=3))
api_request.mount('https://', HTTPAdapter(max_retries=3))

logging.basicConfig(filename=LOG_FOLDER+'log.txt', encoding='utf-8', level=logging.DEBUG)

def download_img(url, path):
    try:
      r = api_request.get(url, timeout=5)
    except exceptions.RequestException as e:
      print(e)
      return
    with open(path,'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)

# def findAllFile(base):
#     for root, ds, fs in os.walk(base):
#         for f in fs:
#             # if filetype.is_video(fullname):
#             if re.search('(\.)(mp4|m4v|mov|qt|avi|flv|wmv|asf|mpeg|mpg|vob|mkv|asf|wmv|rm|rmvb|vob|ts|dat)', f):
#               yield os.path.join(root, f)

# def search_video(path: str):
#   video = Video(path)
#   video.get_data()
#   video.match()
#   insert_data(video)

# def mult_thread(path: str):
#   th = ThreadPoolExecutor()
#   th.map(search_video, findAllFile(path))

# if __name__ == '__main__':
#   # path = r"Z:\video\bangumi\黄金神威\[HYSUB]Golden Kamuy[01v2][GB_MP4][1280X720].mp4"
#   path = 'Z:\\video\\'
#   count = 0
#   s = time.time()
#   for i in findAllFile(path):
#     count += 1
#     # print(i)
#   e = time.time()

#   print(e-s, count)