# %%
import requests
import os
from hashlib import md5
# import cv2
from difflib import SequenceMatcher
from requests.adapters import HTTPAdapter
import json
from config import *
from utils import api_request, download_img
# from data import insert_data

# %%
class Video():
  def __init__(self,path: str) -> None:
    self.path = path
    self.anime_name = []
    self.match_mode = "hashAndFileName"
    self.file_name = os.path.split(self.path)[-1]
    
    
    self.dan_match_api = DAN_MATCH_API
    self.dan_bgm_api = DAN_BGM_API
    self.bgm_bgm_api = BGM_BGN_API
    
    self.match_data =  {
      "fileName": self.file_name,
      "fileHash": '00000000000000000000000000000000',
      "fileSize": 0,
      "videoDuration": 0,
      "matchMode": 'fileName'
      }
  
  def get_md5value(self):
    m = md5()
    video_file = open(self.path, 'rb')
    m.update(video_file.read())
    video_file.close()
    self.file_hash = m.hexdigest()

  def get_video_duration(self):
    cap = cv2.VideoCapture(self.path)
    if cap.isOpened():
      rate = cap.get(5)
      frame_num =cap.get(7)
      duration = frame_num/rate
      self.video_duration:int = duration
    else :
      self.video_duration = 0

  def get_file_size(self):
      self.file_size = os.path.getsize(self.path)
  
  def get_data(self):
    self.get_file_size()
    self.get_md5value()
    self.get_video_duration()

    self.match_data = {
      "fileName": self.file_name,
      "fileHash": self.file_hash,
      "fileSize": self.file_size,
      "videoDuration": self.video_duration,
      "matchMode": self.match_mode
      }

  def update(self,match_request):
    
    episode_info = match_request['matches'][0]
    # print(episode_info)
    self.local_video = episode_info
    self.local_video['path'] = self.path
    del self.local_video['type']
    del self.local_video['shift']

    try:
      dan_bgm_info = api_request.get(self.dan_bgm_api + str(episode_info['animeId']), timeout=5).json()
    except requests.exceptions.RequestException as e:
      print(e)
      return

    # print(json.dumps(dan_bgm_info))
    if dan_bgm_info.get('success', False):
      for i in dan_bgm_info['bangumi']['metadata']:
        if '中文名' in i:
          self.anime_name.append(i[4:])
        elif '别名' in i:
          self.anime_name.append(i[3:])
    
    self.local_video['matchRate'] = self.match_rate()

    self.tvshow  = {}
    for (key ,value) in dan_bgm_info['bangumi'].items() :
      if key in ('animeTitle', 'imageUrl','imagePath', 'animeId', 'typeDescription', 
                'summary', 'bangumiUrl'):
        self.tvshow[key] = value
        
    for i in dan_bgm_info['bangumi']['episodes']:
      if i['episodeId'] == episode_info['episodeId']:
        if 'path' in i:
          i['path'].append(self.path)
        else :
          i['path'] = [self.path]
      
    self.tvshow['episodes'] =  json.dumps(dan_bgm_info['bangumi']['episodes'])
    self.tvshow['metadata'] = json.dumps(dan_bgm_info['bangumi']['metadata'])
    self.tvshow['ratingDetails'] = json.dumps(dan_bgm_info['bangumi']['ratingDetails'])

    img_path = IMG_FOLDER + self.tvshow['animeTitle']+'.'+self.tvshow['imageUrl'].split('.')[-1]
    download_img(self.tvshow['imageUrl'], img_path)
    self.tvshow['imagePath'] = img_path
    

  def match(self):
    # match_request = requests.post(self.dan_match_api, data=self.match_data).json()
    try:
      match_request = api_request.post(self.dan_match_api, data=self.match_data, timeout=5).json()
    except requests.exceptions.RequestException as e:
      print(e)
      return

    if match_request.get('success', False) and len(match_request['matches']):
      # print('dandan request match success')
      self.update(match_request)
  
  def match_rate(self):
    max = 0
    split_name = []
    st = 0
    for index, chr in enumerate(self.file_name):
        if index and chr in PUN:
            split_name.append(self.file_name[st:index])
            st = index
    split_name.extend(self.path.split('\\'))
    split_name.extend(self.path.split('/'))
    max = 0
    sname = [0,1]
    for i in self.anime_name:
        for j in split_name:
            ans = SequenceMatcher(lambda x: x in PUN, j,i).ratio()
            ans2 = SequenceMatcher(lambda x: x in PUN, i,j).ratio()
            if max < ans :
                max = ans 
                sname[0],sname[1] = j, i 
            if max < ans2:
                max = ans2
                sname[0],sname[1] = i,j
    return max
 
  

# %%
# a = requests.post(DAN_MATCH_API + '161720012').json()






