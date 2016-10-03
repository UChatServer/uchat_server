#python
# coding:utf8
import web
from uchatserver import *
from uchatdb import *
import json

##返回信息
##{"code": num,
## "result": value
## "err_str": str
##}
## code信息
##1表示执行操作成功,result中为返回的数据
##0表示执行操作失败，err_str中会有错误提示




app_key = "x18ywvqf8x8rc"
app_secret = "I5Rty3m89YC"

ucs = UChatServer(app_key, app_secret)
ucdb = UChatDB(dbname = 'uchat', username = 'uchat', password = 'uchat', host = '121.42.161.150')

urls = (
    '/login', 'login',
    '/register', 'register',
    '/logout', 'logout',
    '/reconnect', 'reconnect',
)

class login:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.id
        password = i.pwd

        web.header('content-type','text/json')
        rs = ucdb.canlogin(userid, password)
        if rs[0] is False:
            error_str = "不能登录：%s" % rs[1]
            return json.dumps({"code":0, "result":"null", "err_str": error_str})
        else:
            #检查是否在线
            rs = ucs.User.checkOnline(userid)
            if rs.result[u'code'] is 200:
                if rs.result[u'status'] is '1':
                    online = True
                else:
                    online = False
            else:
                online = False
            if online is False:
                username = "kongyt"
                iconurl = 'http://www.rongcloud.cn/images/logo.png'
                rs = ucs.User.getToken(userid, username , iconurl)
                print rs
                if rs.result[u'code'] is 200:
                    ucdb.online(userid, rs.result[u'token'])
                    return json.dumps({"code":1, "result": rs.result[u'token'], "err_str": "null"})
                else:
                    error_str = "登录失败：融云服务返回Token失败"
                    return json.dumps({"code":0, "result": "null", "err_str": error_str})
            else:
                error_str =  "登录失败：用户已经在线"
                return json.dumps({"code":0, "result": "null", "err_str": error_str})
class register:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.id
        password = i.pwd
        web.header('content-type','text/json')
        rs = ucdb.register(userid, password)
        if rs[0] is False:
            error_str = "注册失败：%s" % rs[1]
            return json.dumps({"err_code":0, "result":False, "err_str": error_str})
        else:
            return json.dumps({"err_code":1, "result":True, "err_str": "null"})


class logout:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.id
        usertoken = i.token
        web.header('content-type','text/json')
        rs = ucdb.isonline(userid, usertoken)
        if rs[0] is False:
            error_str = '退出失败：%s' % rs[1]
            return json.dumps({"err_code":0, "result":False, "err_str": error_str})
        else:
            rs = ucdb.logout(userid, usertoken)
            if rs[0] is False:
                error_str = "退出失败：%s" % (rs[1])
                return json.dumps({"err_code":0, "result":False, "err_str": error_str})
            else:
                return json.dumps({"err_code":1, "result":True, "err_str": "null"})

class reconnect:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.id
        usertoken = i.token
        web.header('content-type','text/json')
        rs = ucdb.isonline(userid, usertoken)
        if rs[0] is True:
            username = "kongyt"
            iconurl = 'http://www.rongcloud.cn/images/logo.png'
            rs = ucs.User.getToken(userid, username , iconurl)
            print rs
            if rs.result[u'code'] is 200:
                ucdb.online(userid, rs.result[u'token'])
                return json.dumps({"code":1, "result": rs.result[u'token'], "err_str": "null"})
            else:
                error_str = "登录失败：融云服务返回Token失败"
                return json.dumps({"code":0, "result": "null", "err_str": error_str})
        else:
            error_str = "用户不在线，不能重新换取token"
            return json.dumps({"code":0, "result": "null", "err_str": error_str})




if __name__=="__main__":
    app = web.application(urls, globals())
    app.run()
