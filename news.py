import httplib2
import requests
import time
import os

while True:
    URL_VK = 'https://api.vk.com/method/wall.get?domain=surfcoffee&count=10&v=5.74&filter=owner&access_token=012c6a2d9bad7caebbe3e95a23a23e8f0dca7abe2b3d1bcc2b893d590f223af1a1e928d87583a96713200'
    w = {}
    l = requests.get(URL_VK, params=w)
    data2 = l.json()
    for i in range(10):
        try:
            s1 = 'C:/Users/Ivan/PycharmProjects/location/photo/news1.'+ str(i) +'.jpg'
            url = str(data2['response']['items'][1]['attachments'][i]['photo']['photo_604'])
            h = httplib2.Http('.cache')
            response, content = h.request(url)
            out = open(s1, 'wb')
            out.write(content)
            out.close()
        except Exception:
            try:
                os.remove('C:/Users/Ivan/PycharmProjects/location/photo/news1.'+ str(i) +'.jpg')
            except Exception:
                print()

        try:
            s2='C:/Users/Ivan/PycharmProjects/location/photo/news2.'+ str(i) +'.jpg'
            url = str(data2['response']['items'][2]['attachments'][i]['photo']['photo_604'])
            h = httplib2.Http('.cache')
            response, content = h.request(url)
            out = open(s2, 'wb')
            out.write(content)
            out.close()
        except Exception:
            try:
                os.remove('C:/Users/Ivan/PycharmProjects/location/photo/news2.'+ str(i) +'.jpg')
            except Exception:
                print()

        try:
            s3 = 'C:/Users/Ivan/PycharmProjects/location/photo/news3.'+ str(i) +'.jpg'
            url = str(data2['response']['items'][3]['attachments'][i]['photo']['photo_604'])
            h = httplib2.Http('.cache')
            response, content = h.request(url)
            out = open(s3, 'wb')
            out.write(content)
            out.close()
        except Exception:
            try:
                os.remove('C:/Users/Ivan/PycharmProjects/location/photo/news3.'+ str(i) +'.jpg')
            except Exception:
                print()

    time.sleep(60*30)
