# import urllib, urllib2, cookielib, re
#
# cj = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#
# home = opener.open('https://foobar.com/account/signin.jsp')
# for c in cj:
#     if c.name == "JSESSIONID":
#         jsessionid = c.value
#
# print jsessionid
#
# url = 'https://foobar.com/account/signin.jsp'
# page = opener.open(url).read()
# dynSessConf = re.findall(r'input name="_dynSessConf" value="(.*)" type="hidden"', page)
#
# data = urllib.urlencode({"email": "a@a.com",
#                          "password": "barfoo",
#                          "_D:email": "+",
#                          "_D:password": "+",
#                          "_D:/atg/userprofiling/ProfileFormHandler.login": "+",
#                          "_DARGS": "/account/signin.jsp.loginForm",
#                          "/atg/userprofiling/ProfileFormHandler.login": "Sign+in"})
#
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# opener.addheaders.append(('User-agent', 'Mozilla/5.0'))
# opener.addheaders.append(('Referer', 'https://foobar.com/account/signin.jsp'))
# opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
# request = urllib2.Request("https://foobar.com/account/actions/login-submit.jsp?_DARGS=/account/signin.jsp.loginForm",
#                           data)
# response = opener.open(request)
#
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# opener.addheaders.append(('User-agent', 'Mozilla/5.0'))
# opener.addheaders.append(
#     ('Referer', 'https://foobar.com/account/actions/login-submit.jsp?_DARGS=/account/signin.jsp.loginForm'))
# opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
# request = urllib2.Request("https://foobar.com/account/foobaz-next.jsp")
# response = opener.open(request)
# # page = opener.open(url).read()
#
# j = None
# for h in response.info().headers:
#     if h.find("JSESSIONID") > -1:
#         j = h
#
# if j != None:
#     print
#     "JSESSIONID changed from ", jsessionid, " to ", j
# else:
#     print
#     "JSESSIONID persisted as ", jsessionid, " throughout the session"
