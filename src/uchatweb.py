#python
# coding:utf8
import web
from uchatserver import *
from uchatdb import *
import json


app_key = "x18ywvqf8x8rc"
app_secret = "I5Rty3m89YC"

ucs = UChatServer(app_key, app_secret)
ucdb = UChatDB(dbname = 'uchat', username = 'uchat', password = 'uchat', host = '192.168.0.102')

urls = (
    '/login', 'login',
    '/register', 'register',
    '/logout', 'logout',
    '/reconnect', 'reconnect',
)

class login:
    def GET(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.user_id
        password = i.user_password
        rs = ucdb.canlogin(userid, password)
        if rs[0] is False:
            return ("不能登录：%s" % rs[1]).decode("utf8").encode('gb2312')
        else:
            rs = ucdb.isonline(userid)
            if rs[0] is False:
                username = "kongyt"
                iconurl = 'http://www.rongcloud.cn/images/logo.png'
                rs = ucs.User.getToken(userid, username , iconurl)
                print rs
                if rs.result[u'code'] is 200:
                    ucdb.online(userid, rs.result[u'token'])
                    return "成功".decode("utf8").encode('gb2312')+str(rs)
                else:
                    return "登录失败：融云服务返回Token失败".decode("utf8").encode('gb2312')+str(rs)
            else:
                return "登录失败：用户已经在线".decode('utf8').encode('gb2312')
class register:
    def GET(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.user_id
        password = i.user_password
        rs = ucdb.register(userid, password)
        if rs[0] is False:
            return ("注册失败：%s" % rs[1]).decode('utf8').encode('gb2312')
        else:
            return "注册成功".decode('utf8').encode('gb2312')


class logout:
    def GET(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.user_id
        usertoken = i.user_token
        rs = ucdb.isonline(userid)
        if rs[0] is False:
            return ('退出失败：%s' % rs[1]).decode('utf8').encode('gb2312')
        else:
            rs = ucdb.logout(userid, usertoken)
            if rs[0] is False:
                return ("退出失败：%s" % (rs[1])).decode('utf8').encode('gb2312')
            else:
                return "退出成功".decode('utf8').encode('gb2312') 

class reconnect:
    def GET(self):
        return "敬请期待".decode('utf8').encode('gb2312')




if __name__=="__main__":
    app = web.application(urls, globals())
    app.run()
