

import requests
import re
from PIL import Image
import string
import random
import time

# from selenium.webdriver.common.action_chains import ActionChains
# from selenium import webdriver
# # chars = string.ascii_letters + string.digits
# mypath = ''
# driver = webdriver.PhantomJS(mypath)
# actions = ActionChains(driver)
# driver.get('https://unsplash.com/t/wallpapers')
#
# for _ in range(1000):
#     driver.execute_script('window.scrollTo(0,1000000)')
#     time.sleep(0.2)
#
#
#
# res = requests.get('https://unsplash.com/t/wallpapers')
# l1 = re.findall(r'"href=/photos/(\w+)"', res.text)
# index_urls = ["https://unsplash.com/photos/{}".format(x) for x in l1]
#
# images_urls = []
#
# for x in index_urls:
#     res = requests.get(x)
#     real_url = re.findall(r'srcSet="(.+?)"', res.text)[1] #list里面好像 list[1]=list[2]
#     images_urls.append((x, real_url))#['gssfe...', 'http://...']
#
#
# for name, x in images_urls:
#     try:
#         res = requests.get(x)
#         # name = random.choices(chars, k=12)
#         with open(name+'.jpg', 'w') as fp:
#             fp.write(res.content)
#         print('write image name:', name+'.jpg')
#     except Exception as e:
#         pass


chars = string.ascii_letters+string.digits
headers = {"User-Agent": "PostmanRuntime/7.30.1",
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive'}
url = "https://bing.ioliu.cn/v1/rand?w=560&h=400"
requests.packages.urllib3.disable_warnings()
for _ in range(0):
    res = requests.get(url, headers = headers, verify=False)
    name = ''.join(random.choices(chars,k=20))
    if res.status_code == 200:
        with open('static/img/headimgs/'+name+'.jpg', 'wb') as fp:
            fp.write(res.content)
    else:
        print(res.status_code, res)

url = "https://bing.ioliu.cn/v1/rand?w=1024&h=633"
requests.packages.urllib3.disable_warnings()
for _ in range(5):
    res = requests.get(url, headers = headers, verify=False)
    name = ''.join(random.choices(chars,k=20))
    if res.status_code == 200:
        with open('static/img/blogimgs/'+name+'.jpg', 'wb') as fp:
            fp.write(res.content)
    else:
        print(res.status_code, res)
