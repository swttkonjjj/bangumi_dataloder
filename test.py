import time
from libery import mult_thread
from data import initdb

  # path = r"Z:\video\bangumi\黄金神威\[HYSUB]Golden Kamuy[01v2][GB_MP4][1280X720].mp4"
path = 'Z:\\video\\download'
count = 0
initdb()
s = time.time()
mult_thread(path)
e = time.time()

print(e-s, count)