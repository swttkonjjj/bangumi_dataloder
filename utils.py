from requests import Session, exceptions
from requests.adapters import HTTPAdapter

api_request = Session()
api_request.mount('http://', HTTPAdapter(max_retries=3))
api_request.mount('https://', HTTPAdapter(max_retries=3))

def download_img(url, path):
    try:
      r = api_request.get(url, timeout=5)
    except exceptions.RequestException as e:
      print(e)
      return
    with open(path,'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)