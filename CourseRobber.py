import http.cookiejar
import urllib.request
import os

from bs4 import BeautifulSoup
import json
import time


class CourseRobber:

    def __init__(self):

        self.info = {
            'username': '',
            'password': ''
        }
        self.course = {
            'property': '',
            'belong': '',
            'category': '',
            'teacher': '',
            'day': '',
            'time': ''
        }
        self.priority = []
        self.period = 1
        self.curCourse = {
            'name': '',
            'id': '',
            'priority': -1
        }

        cookiejar = http.cookiejar.CookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookiejar)
        self.opener = urllib.request.build_opener(handler)

        self.attribute_map = {
            "": "",

            "校公选课": "06",
            "拓展英语": "02",

            "文化素质通识课": "1",
            "实践训练通识课": "2",
            "特殊课程": "3",
            "专项英语": "4",
            "通识教育选修课": "5",
            "专项数学": "6",
            "实验选修课": "7",
            "普通类通识教育选修课": "8",
            "艺术类通识教育选修课": "9",

            "艺术实践": "7",
            "创新与创业": "6",
            "哲学与历史": "1",
            "文学与艺术": "2",
            "健康与社会": "3",
            "经济与管理": "4",
            "科学与技术": "5",
            "文化实践": "9",
            "科技实践": "8",

            "星期一": "1",
            "星期二": "2",
            "星期三": "3",
            "星期四": "4",
            "星期五": "5",
            "星期六": "6",
            "星期日": "7",

            "1-2节": "1-2",
            "3-4-5节": "3-4",
            "6-7节": "6-7",
            "8-9节": "8-9-10",
            "11-12节": "11-12-13"
        }

    def load_conf(self, conf_path):
        print("[打开配置文件] " + conf_path)
        try:
            conf_file = open(conf_path, 'r', encoding='utf-8')
            conf = json.loads(conf_file.read())
            print('[读取配置文件]')
            print('{')

            self.info['username'] = conf['用户名']
            self.info['password'] = conf['密码']
            print('    "用户名": "' + self.info['username'] + '",')
            print('    "密码": "' + len(self.info['password']) * '*' + '",')

            self.course['property'] = conf['课程性质']
            self.course['belong'] = conf['课程归属']
            self.course['category'] = conf['种类']
            self.course['teacher'] = conf['上课老师']
            self.course['day'] = conf['星期']
            self.course['time'] = conf['上课节次']
            print('    "课程性质": "' + self.course['property'] + '",')
            print('    "课程归属": "' + self.course['belong'] + '",')
            print('    "种类": "' + self.course['category'] + '",')
            print('    "上课老师": "' + self.course['teacher'] + '",')
            print('    "星期": "' + self.course['day'] + '",')
            print('    "上课节次": "' + self.course['time'] + '",')

            self.priority = conf['课程优先级']
            print('    "课程优先级": [')
            for course in self.priority[:-1]:
                print('        "' + course + '",')
            print('        "' + self.priority[-1] + '"')
            print('    ],')

            self.period = conf['刷新周期']
            print('    "刷新周期": "' + str(self.period) + '"')

            print('}')
            print('[读取配置文件完成]\n')

        except IOError:
            print("[打开配置文件失败]")
            return False
        finally:
            conf_file.close()
        return True

    def login(self):
        print('[正在登陆] 用户名: ' + self.info['username'])

        # 访问登陆页面获取lt和execution值
        url = 'https://login.bit.edu.cn/cas/login'
        request = urllib.request.Request(url)
        html = self.opener.open(request).read().decode()

        soup = BeautifulSoup(html, 'lxml')
        f = soup.find('form')
        lt = f.find('input', type='hidden')['value']
        execution = f.find('input', type='hidden').next_element.next_element['value']

        data = {
            'username': self.info['username'],
            'password': self.info['password'],
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit',
            'rmShown': '1'
        }
        data = urllib.parse.urlencode(data).encode()

        # 登陆
        request = urllib.request.Request(url, data)
        html = self.opener.open(request).read().decode()

        result = True;
        if result:
            print('[登陆成功]\n')
        else:
            print('[登陆失败]')
        return result



    def rob_init(self):
        print('[抢课前初始化]')

        # 访问教务管理系统主页
        url = 'http://jwms.bit.edu.cn/'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        request = urllib.request.Request(url, headers=headers)
        self.opener.open(request);

        # 访问选课入口页面
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=5AD7F2B38FF94371BD3F8C5EC665C415'
        request = urllib.request.Request(url)
        self.opener.open(request)

        # 访问公共课选课页面
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk'
        request = urllib.request.Request(url)
        self.opener.open(request).read().decode()

        print('[抢课前初始化完成]\n')

    def pull_course_list(self):
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?'
        url = url + 'kcxx='
        url = url + '&skls=' + self.course['teacher']
        url = url + '&kcxz=' + self.attribute_map[self.course['property']]
        url = url + '&kcgs=' + self.attribute_map[self.course['belong']]
        url = url + '&szjylb=' + self.attribute_map[self.course['category']]
        url = url + '&skxq=' + self.attribute_map[self.course['day']]
        url = url + '&skjc=' + self.attribute_map[self.course['time']]
        url = url + '&sfym=true&sfct=false'

        data = {
            'iDisplayStart': '0',
            'iDisplayLength': '1000',
        }
        data = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(url, data)
        course_json = self.opener.open(request).read().decode()
        courses = json.loads(course_json)['aaData']
        return courses

    def get_curCourse(self):
        print('[正在获取已选课信息]')

        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkjg/comeXkjglb'
        request = urllib.request.Request(url)
        html = self.opener.open(request).read().decode()
        soup = BeautifulSoup(html, 'lxml')
        tr_list = soup.table.tbody.find_all('tr')

        if self.course['property'] == '':
            self.course['property'] = '体育课'

        for tr in tr_list:
            if str(tr).find('专业课') > -1:
                continue
            if str(tr).find(self.course['property']) > -1 and \
                    str(tr).find(self.course['belong']) > -1:
                td_list = tr.find_all('td')
                self.curCourse['name'] = td_list[1].string[:-5]
                self.curCourse['id'] = td_list[-1].a['href'][-18:-3]
                break

        if self.course['property'] == '体育课':
            self.course['property'] = ''

        if self.curCourse['name'] in self.priority:
            self.curCourse['priority'] = self.priority.index(self.curCourse['name'])

        print('    已选课程: ', end='')
        if self.curCourse['name'] == '':
            print('无')
        else:
            print(self.curCourse['name'] + ' 优先级: ' + str(self.curCourse['priority']));

        print('[获取已选课信息完成]\n')

    def rob(self):
        self.rob_init()
        self.get_curCourse()

        while self.curCourse['priority'] != 0:
            course_list = self.pull_course_list()

            print('[获取课程列表] ' + '选候课程: ' + str(len(course_list)))
            print('已选课程: ', end='')
            if self.curCourse['name'] == '':
                print('无')
            else:
                print(self.curCourse['name']);

            for course in course_list:
                print('    ' + course['kcmc'] + ' 剩余: ' + course['syrs'])

                if course['kcmc'] in self.priority:
                    if self.curCourse['priority'] == -1:
                        result = self.rob_course(course['jx0404id'])
                        if result['success']:
                            self.curCourse['name'] = course['kcmc']
                            self.curCourse['id'] = course['jx0404id']
                            self.curCourse['priority'] = self.priority.index(self.curCourse['name'])
                            print('>>>抢到课程 ' + self.curCourse['name'] + '<<<')
                        else:
                            print('>>>抢课失败 ' + result['message'])

                    elif self.priority.index(course['kcmc']) < self.curCourse['priority']:

                        result = self.drop_course(self.curCourse['id'])
                        if result['success']:
                            print('>>>退掉课程 ' + self.curCourse['name'] + '<<<')
                            self.curCourse['name'] = ''
                            self.curCourse['id'] = ''
                            self.curCourse['priority'] = -1
                        else:
                            print('>>>退课失败 ' + result['message'])

                        result = self.rob_course(course['jx0404id'])
                        if result['success']:
                            print('>>>抢到课程 ' + self.curCourse['name'] + '<<<')
                            self.curCourse['name'] = course['kcmc']
                            self.curCourse['id'] = course['jx0404id']
                            self.curCourse['priority'] = self.priority.index(self.curCourse['name'])
                        else:
                            print('>>>抢课失败 ' + result['message'])


            time.sleep(self.period)
            print()
        return True

    def rob_course(self, course_id):
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/ggxxkxkOper'
        data = {'jx0404id': course_id}
        data = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(url, data)
        result = self.opener.open(request).read().decode()
        result = json.loads(result)
        return result

    def drop_course(self, course_id):
        url = 'http://jwms.bit.edu.cn/jsxsd/xsxkjg/xstkOper'
        data = {'jx0404id': course_id}
        data = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(url, data)
        result = self.opener.open(request).read().decode()
        result = json.loads(result)
        return result


if __name__ == '__main__':
    try:
        courseRobber = CourseRobber()
        courseRobber.load_conf('CourseRobber.json')
        courseRobber.login()
        courseRobber.rob()
    except Exception as e:
        print(e)
    os.system('pause')

