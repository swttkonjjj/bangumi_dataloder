import re
from video import Video
import os
from data import insert_data
from concurrent.futures import ThreadPoolExecutor
from data import insert_data
import time
from utils import logging
import threading
import itertools

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            # if filetype.is_video(fullname):
            if re.search('(\.)(mp4|m4v|mov|qt|avi|flv|wmv|asf|mpeg|mpg|vob|mkv|asf|wmv|rm|rmvb|vob|ts|dat)', f):
              yield os.path.join(root, f)

def search_video(path: str,lock):
  video = Video(path)
  # video.get_data()
  video.match()
  # with threading.Lock():
  with lock:
    insert_data(video)

def mult_thread(path: str):
  # th = ThreadPoolExecutor()
  # th.map(search_video, findAllFile(path))
  lock = threading.Lock()
  with ThreadPoolExecutor(max_workers=min(10, (os.cpu_count() or 1) + 4)) as executor:
    for i in executor.map(search_video, findAllFile(path), itertools.repeat(lock)):
      logging.info(i)

if __name__ == '__main__':
  # path = r"Z:\video\bangumi\黄金神威\[HYSUB]Golden Kamuy[01v2][GB_MP4][1280X720].mp4"
  path = 'Z:\\video\\download'
  count = 0
  s = time.time()
  mult_thread(path)
  e = time.time()

  print(e-s, count)