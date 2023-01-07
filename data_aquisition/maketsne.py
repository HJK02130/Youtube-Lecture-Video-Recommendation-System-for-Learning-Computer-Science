import json
from PIL import Image
import numpy as np
import requests
import cv2
with open("videos.json", "r") as jsonfile:
  data = json.load(jsonfile)


videolist = list(data["videos"].keys())
imagelist = []
c = 0
for vid in videolist:
    
    
    url = data["videos"][vid]["thumbnails"]
    im = Image.open(requests.get(url, stream=True).raw)
    imarray = np.asarray(im)
    
    if not imarray.shape == (360,480,3):
        imarray = cv2.resize(imarray, (480,360), interpolation=cv2.INTER_CUBIC)
    assert imarray.shape == (360,480,3)
    imagelist.append(imarray)
    c += 1
    print("{}: {}".format(c, np.asarray(imagelist).shape))
    

imagelist = np.asarray(imagelist)

np.save("images", imagelist)

loadfile = np.load("images.npy")
print(loadfile.shape)