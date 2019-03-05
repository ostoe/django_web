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
url = "https://api.berryapi.net/bing/random/?560/400"
for _ in range(200):
    res = requests.get(url)
    name = ''.join(random.choices(chars,k=20))
    with open('static/img/headimgs/'+name+'.jpg', 'wb') as fp:
        fp.write(res.content)



from scipy.interpolate import interp2d
interp2d
