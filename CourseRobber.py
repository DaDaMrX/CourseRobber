import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup

url = 'https://login.bit.edu.cn/cas/login'

cookiejar = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookiejar)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(url)
html = opener.open(request).read().decode()

soup = BeautifulSoup(html, 'lxml')
f = soup.find('form')
lt = f.find('input', type='hidden')['value']
# print(lt)
execution = f.find('input', type='hidden').next_element.next_element['value']
# print(execution)

data = {
    'username': '1120151811',
    'password': '151886',
    'lt': lt,
    'execution': execution,
    '_eventId': 'submit',
    'rmShown': '1'
}
data = urllib.parse.urlencode(data).encode()

request = urllib.request.Request(url, data)

a = opener.open(request)
html = a.read().decode()

url = 'http://jwms.bit.edu.cn/'
request = urllib.request.Request(url)
html = opener.open(request).read().decode()

url = 'http://jwms.bit.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=5AD7F2B38FF94371BD3F8C5EC665C415'
request = urllib.request.Request(url)
html = opener.open(request).read().decode()

url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk'
request = urllib.request.Request(url)
html = opener.open(request).read().decode()

url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=&kcxz=06&kcgs='
data = {
    'sEcho': '1',
    'iColumns': '14',
    'sColumns': '',
    'iDisplayStart': '0',
    'iDisplayLength': '15',
    'mDataProp_0': 'kch',
    'mDataProp_1': 'kcmc',
    'mDataProp_2': 'bhbm',
    'mDataProp_3': 'kcsxmc',
    'mDataProp_4': 'kcgsmc',
    'mDataProp_5': 'szkcflmc',
    'mDataProp_6': 'xf',
    'mDataProp_7': 'skls',
    'mDataProp_8': 'sksj',
    'mDataProp_9': 'skdd',
    'mDataProp_10': 'xkrs',
    'mDataProp_11': 'syrs',
    'mDataProp_12': 'ctsm',
    'mDataProp_13': 'czOper',
}
data = urllib.parse.urlencode(data).encode()
request = urllib.request.Request(url, data)
html = opener.open(request).read().decode()

url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/ggxxkxkOper'
data = {
    'jx0404id': '201720182002226',
    'xkzy': '',
    'trjf': ''
}
data = urllib.parse.urlencode(data).encode()
request = urllib.request.Request(url, data)
html = opener.open(request).read().decode()

print(html)
# a = open('a.html', 'w')
# a.write(html)

print("Done!")
