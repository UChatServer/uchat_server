#! python
# coding:utf8

import web

class UChatDB():
    def __init__(self, dbname, username, password,  host):
        self._db = web.database(dbn = 'mysql', db = dbname, user = username, pw = password, host = host)

    def isonline(self, userid):
        rs = self._db.query('select id, user_online from uchat.user_info where user_id = $uid', vars = {'uid': userid})
        if len(rs) == 0:
            return (False, "用户不存在")
        online = rs[0].user_online
        print '[是否在线]:',online
        if online == u'Y':
            return (True, "用户在线")
        else:
            return (False, "用户不在线")

    def online(self, userid, token):
        rs = self._db.update('user_info', where='user_id=$uid', vars = {'uid': userid}, user_online = u'Y', user_token = token)

    def logout(self, userid, token):
        rs =  self._db.query('select id, user_online from uchat.user_info where user_id = $uid and user_token = $utoken', vars = {'uid': userid, 'utoken': token})
        if len(rs) == 0:
            return (False, "用户不存在或token错误")
        else:
            self._db.update('user_info', where='id = $tid', vars={'tid': rs[0].id}, user_online = u'N')
            return (True, "退出成功")
            

    def canlogin(self, userid, password):
        rs = self._db.query('select id, user_token, user_online from uchat.user_info where user_id = $uid and user_password = $pw', vars={'uid': userid, 'pw': password})
        if len(rs) == 0:
            print "[登录失败]：用户名或密码错误"
            return (False, "用户名或密码错误")
        else:
            print "[可以登录]"
            return (True , "可以登录")

    def register(self, userid, password):
        rs = self._db.query('select id from uchat.user_info where user_id = $uid', vars={'uid': userid})
        if len(rs) == 0:
            rs = self._db.insert('user_info', user_id = userid, user_password = password, user_online = 'N')
            print "[注册成功]"
            return (True, "注册成功")
        else:
            print "[注册失败]：用户已经存在！"
            return (False, "用户已经存在")

