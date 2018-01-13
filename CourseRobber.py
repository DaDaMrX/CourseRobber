import http.cookiejar
import urllib.request

import os
from bs4 import BeautifulSoup
import json
import time


class CourseRobber:

    def __init__(self, confPath):
        # 读取配置文件
        self.conf = open(confPath, encoding='utf-8').read()
        self.conf = json.loads(self.conf)

        self.opener = None
        self.curCourseId = None
        self.curCourseName = None
        self.curCoursePriority = -1

        self.log = open('log.txt', 'w', encoding='utf-8')

    def login(self):
        # 创建opener存储cookie
        cookiejar = http.cookiejar.CookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookiejar)
        self.opener = urllib.request.build_opener(handler)

        # 访问登陆页面获取lt和execution值
        url = 'https://login.bit.edu.cn/cas/login'
        request = urllib.request.Request(url)
        html = self.opener.open(request).read().decode()

        soup = BeautifulSoup(html, 'lxml')
        f = soup.find('form')
        lt = f.find('input', type='hidden')['value']
        execution = f.find('input', type='hidden').next_element.next_element['value']

        data = {
            'username': self.conf['username'],
            'password': self.conf['password'],
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit',
            'rmShown': '1'
        }
        data = urllib.parse.urlencode(data).encode()

        # 登陆
        request = urllib.request.Request(url, data)
        html = self.opener.open(request).read().decode()

        # print(html)

        return True

    def robInit(self):
        # 访问教务管理系统主页
        url = 'http://jwms.bit.edu.cn/'
        request = urllib.request.Request(url)
        self.opener.open(request).read().decode()

        # 访问选课入口页面
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=5AD7F2B38FF94371BD3F8C5EC665C415'
        request = urllib.request.Request(url)
        self.opener.open(request).read().decode()

        # 访问公共课选课页面
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk'
        request = urllib.request.Request(url)
        self.opener.open(request).read().decode()

        # 获取当前课程信息
        self.curCourseId, self.curCourseName = self.queryCurCourse()
        if self.curCourseName in self.conf['coursePriority']:
            self.curCoursePriority = self.conf['coursePriority'].index(self.curCourseName)

    def rob(self):
        self.robInit()

        # 不断查询课程信息
        while self.curCoursePriority != 0:
            print("Get course list...")
            # self.log("Get course list..." + '\n')
            # 拉取公共课列表
            url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?' \
                  'kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=&kcxz=06&kcgs='
            data = {
                'iDisplayStart': '0',
                'iDisplayLength': '1000',
            }
            data = urllib.parse.urlencode(data).encode()
            request = urllib.request.Request(url, data)
            courseJson = self.opener.open(request).read().decode()
            courseList = json.loads(courseJson)['aaData']

            # 检索课程列表
            for course in courseList:

                print('    Deal Course: ' + course['kcmc'])
                # self.log('    Deal Course: ' + course['kcmc'] + '\n')

                if course['kcmc'] in self.conf['coursePriority'] and \
                        course['kcgsmc'] == self.conf['courseCategory'] and int(course['syrs']) > 0:
                    if self.curCoursePriority == -1:
                        self.robCourse(course['jx0404id'])
                        self.curCourseName = course['kcmc']
                        self.curCourseId = course['jx0404id']
                        if self.curCourseName in self.conf['coursePriority']:
                            self.curCoursePriority = self.conf['coursePriority'].index(self.curCourseName)
                        print('Get course ' + self.curCourseName + '!')
                    elif self.conf['coursePriority'].index(course['kcmc']) < self.curCoursePriority:
                        self.dropCourse(self.curCourseId)
                        self.robCourse(course['jx0404id'])
                        self.curCourseName = course['kcmc']
                        self.curCourseId = course['jx0404id']
                        self.curCoursePriority = self.conf['coursePriority'].index(self.curCourseName)
                        print('Replace course ' + self.curCourseName + '!')

            # 等待指定时间
            time.sleep(self.conf['refreshPeriod'])
        return True

    def queryCurCourse(self):
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkjg/comeXkjglb'
        request = urllib.request.Request(url)
        html = self.opener.open(request).read().decode()
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)
        trList = soup.table.tbody.find_all('tr')

        courseName = None
        courseId = None
        for tr in trList:
            if str(tr).find(self.conf['courseCategory']) > -1:
                tdList = tr.find_all('td')
                courseName = tdList[1].string[:-5]
                courseId = tdList[-1].a['href'][-18:-3]
        return courseId, courseName

    def robCourse(self, courseId):
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/ggxxkxkOper'
        data = {'jx0404id': courseId}
        data = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(url, data)
        resultJson = self.opener.open(request).read().decode()
        result = json.loads(resultJson)
        return result['success']

    def dropCourse(self, courseId):
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkjg/xstkOper'
        data = {'jx0404id': courseId}
        data = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(url, data)
        resultJson = self.opener.open(request).read().decode()
        result = json.loads(resultJson)
        return result['success']


if __name__ == '__main__':
    courseRobber = CourseRobber('CourseRobber.json')
    print('Read Configuration Successfully.')
    result = courseRobber.login()
    if result:
        print("Login Successfully.")
    result = courseRobber.rob()
    if result:
        print("Rob course Finish!")

    os.system('pause')

