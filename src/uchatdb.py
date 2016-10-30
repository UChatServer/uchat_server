#! python
# coding:utf8

import web

class UChatDB():
    def __init__(self, dbname, username, password,  host):
        self._db = web.database(dbn = 'mysql', db = dbname, user = username, pw = password, host = host)

    def isonline(self, userid, usertoken):
        rs = self._db.query('select id, user_online from uchat.user_info where user_id = $uid and user_token = $utoken', vars = {'uid': userid, 'utoken': usertoken})
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

    def register(self, userid, password, name, birthday, sex):
        try:
            rs = self._db.query('select id from uchat.user_info where user_id = $uid', vars={'uid': userid})
            if len(rs) == 0:
                rs = self._db.insert('user_info', user_id = userid, user_password = password, user_online = 'N', user_name = name, user_birthday = birthday, user_sex = sex)
                print "[注册成功]"
                return (True, "注册成功")
            else:
                print "[注册失败]：用户已经存在！"
                return (False, "用户已经存在")
        except Exception, e:
            err_str = "注册时数据库操作异常"
            print err_str
            return (False, err_str)

    def get_user_info(self, userid):
        rs = self._db.query('select id, user_name, user_sex, user_birthday, user_address, user_hobbies, user_career, user_tags from uchat.user_info where user_id = $uid', vars = {'uid': userid})
        if len(rs) == 0:
            print "[查询角色信息失败]"
            return None
        else:
            print "[查询角色信息成功]"
            return rs[0]

    def set_user_info(self, userid, datamap):
	rs = self._db.update('user_info', where= 'user_id=$uid', vars = {'uid': userid}, **datamap)

    def change_pwd(self, userid, password):
        rs = self._db.update('user_info', where='user_id=$uid', vars = {'uid': userid}, user_password = password)

    def can_get_friend_info(self, userid1, userid2):
        return True

    def add_friend(self, userid1, token, userid2):
        try:
            rs =self.isonline(userid1, token)
            if rs[0] is True:
                rs2 =  self._db.query('select id from uchat.user_friends_info where user1_id = $uid1 and user2_id = $uid2', vars = {'uid1': userid1, 'uid2': userid2})
                if len(rs2) == 0:
                    rs3 = self._db.insert('user_firends_info', user1_id = userid1, user2_id = userid2)
                    rs3 = self._db.insert('user_firends_info', user1_id = userid2, user2_id = userid1)
                    return (True, "添加好友成功")
                else:
                    return (False, "已经是好友了")
            else:
                return (False, "当前用户在线认证失败")
        except Exception, e:
            err_str = "添加好友时数据库操作异常"
            print err_str
            return (False, err_str)

    def del_friend(self, userid1, token, userid2):
        try:
            rs = self.isonline(userid1, token)
            if rs[0] is True:
                rs2 =  self._db.query('select id from uchat.user_friends_info where user1_id = $uid1 and user2_id = $uid2', vars = {'uid1': userid1, 'uid2': userid2})
                if len(rs2) != 0:
                    rs3 = self._db.delete('uchat.user_friends_info', where="user1_id=\"%s\" and user2_id=\"%s\"" % (userid1, userid2))
                    rs4 = self._db.delete('uchat.user_friends_info', where="user1_id=\"%s\" and user2_id=\"%s\"" % (userid2, userid1))
                    print "删除好友成功"
                    return (True, "删除好友成功")
                else:
                    return (False,"双方不是好友")
            else:
                return (False, "当前用户在线认证失败")
        except Exception, e:
            err_str = "删除好友时数据库操作异常"
            print err_str
            return (False, err_str)


    def get_friends(self, userid, token, ofst, lmt):
        try:
            rs = self.isonline(userid, token)
            if rs[0] is True:
                rs2 = self._db.select('uchat.user_friends_info', what='user2_id', where="user1_id=\"%s\"" % (userid), offset=ofst, limit=lmt)
                data = []
                for d in rs2:
                    data.append(d.user2_id)
                return (True, data)
            else:
                return (False, "当前用户在线认证失败")
        except Exception, e:
            err_str = "获取好友时数据库操作异常"
            print err_str
            return (False, err_str)

    def get_recommend_friends(self, userid, token, ofst, lmt):
        try:
            rs = self.isonline(userid, token)
            if rs[0] is True:
                rs2 = self._db.select('uchat.user_info', what='user_id', where="user_id!=\"%s\"" % (userid), offset=ofst, limit=lmt)
                data = []
                for d in rs2:
                    data.append(d.user_id)
                return (True, data)
            else:
                return (False, "当前用户在线认证失败")
        except Exception, e:
            err_str = "匹配好友时数据库操作异常"
            print err_str
            return (False, err_str)

    def lock_pixel(self, userid, utoken, pix_x, pix_y):
        try:
            rs = self.isonline(userid, utoken)
            if rs[0] is True:
                t = self._db.transaction()
		try:
                    rs2 = self._db.query("select id, user_id from uchat.pixel_lock_info where pixel_x= $px and pixel_y=$py for update", vars = {'px': pix_x, 'py': pix_y})
		    if len(rs2) == 0:
                        self._db.insert('uchat.pixel_lock_info', user_id=userid, pixel_x = pix_x, pixel_y = pix_y)
                except:
                    t.rollback()
		    return (False, "像素锁定失败")
                else:
                    t.commit()
                    return (True, "像素锁定成功")
            else:
                return (False, "用户在线认证失败")
        except Exception, e:
            err_str = "锁定像素时数据库操作异常"
	    print err_str
	    return (False, err_str)

    def unlock_pixel(self, userid, utoken, pix_x, pix_y):
        try:
            rs = self.isonline(userid, utoken)
            if rs[0] is True:
                 t = self._db.transaction()
                 try:
                     rs2 = self._db.query("select id from uchat.pixel_lock_info where userid = $uid pixel_x= $px and pixel_y=$py for update", vars = {'uid': userid, 'px': pix_x, 'py': pix_y})
                     if len(rs2) != 0:
                         self._db.delete('uchat.pixel_lock_info', where='id = $tid', vars = {'tid': rs2[0].id})
                 except:
                     t.rollback()
                     return (False, "像素解锁失败")
                 else:
                     t.commit()
                     return (True, "像素解锁成功")
            else:
                return (False, "用户在线认证失败")
        except Exception, e:
            err_str = "解锁像素时数据库操作异常"
            print err_str
            return (False, err_str)


    def buy_pixel(self, userid, utoken, pix_x, pix_y):
	try:
            rs = self.isonline(userid, utoken)
            if rs[0] is True:
                t = self._db.transaction()
                try:
                    rs2 = self._db.query("select id, user_id from uchat.pixel_lock_info where pixel_x= $px and pixel_y=$py for update", vars = {'px': pix_x, 'py': pix_y})
                    if len(rs2) != 0:
                        if self.pixel_wall_version_add_one()[0] is True:
                            self._db.update('uchat.pixel_lock_info', what='isbuy=$b', vars = {'b': 'Y'}, id=rs[0].id)
                        else:
                            return (False, "像素墙版本信息设置错误")
                except:
                    t.rollback()
                    return (False, "像素购买失败")
                else:
                    t.commit()
                    return (True, "像素购买成功")
            else:
                return (False, "用户在线认证失败")
        except Exception, e:
            err_str = "像素购买时数据库操作异常"
            print err_str
            return (False, err_str)


    def get_pixel_wall_version(self):
        try:
            rs = self._db.query('select pixel_version from uchat.global_info where id = 1')
            if len(rs) != 0:
                return (True, rs[0].pixel_version)
            else:
                return (True, 0)
        except Exception, e:
            err_str = "获取像素墙版本信息时数据库操作异常"
            print err_str
            return (False, err_str)

    def pixel_wall_version_add_one(self):
        try:
            rs = self.get_pixel_wall_version()
            if rs[0] is True:
                 if rs[1] != 0:
                     self._db.update("uchat.global_info", where='id=1', pixel_version = (rs[1]+1))
                     return (True, rs[1]+1)
                 else:
                     return (False, "像素墙版本在数据库中的信息初始化错误")
             else:
                 return (False, "像素墙版本在数据库中的信息尚未初始化")
        except Exception, e:
            err_str = "设置像素墙版本信息时数据库操作异常"
            print err_str
            return (False, err_str)
