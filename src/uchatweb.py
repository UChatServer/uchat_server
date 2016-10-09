#python
# coding:utf8
import web
from uchatserver import *
from uchatdb import *
import json
from PIL import Image
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
    '/uploadimg', 'uploadimg',
    '/images/(.*)', 'getimage',
    '/get_self_info', 'get_self_info',
    '/get_friend_info', 'get_friend_info',
    '/set_user_info', 'set_user_info',
    '/change_password_by_old_pwd', 'change_password_by_old_pwd',
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
            return json.dumps({"err_code":0, "result":"null", "err_str": error_str})
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
                    return json.dumps({"err_code":1, "result": rs.result[u'token'], "err_str": "null"})
                else:
                    error_str = "登录失败：融云服务返回Token失败"
                    return json.dumps({"err_code":0, "result": "null", "err_str": error_str})
            else:
                error_str =  "登录失败：用户已经在线"
                return json.dumps({"err_code":0, "result": "null", "err_str": error_str})
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

class get_self_info:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.id
        usertoken = i.token
        web.header('content-type','text/json')
        if ucdb.isonline(userid, usertoken)[0] is False:
            error_str = "获取个人信息失败，用户token错误"
            return json.dumps({"err_code": 0, "result": {}, "err_str": error_str})          
        rs = ucdb.get_user_info(userid)
        if rs is None:
            error_str = "获取个人信息失败"
            return json.dumps({"err_code": 0, "result": {}, "err_str": error_str})
        else:
            return json.dumps({"err_code": 1, "result": {"user_name": rs.user_name, "user_sex": rs.user_sex, "user_birthday": rs.user_birthday, "user_address": rs.user_address, "user_hobbies": rs.user_hobbies, "user_career": rs.user_career, "user_constellation": rs.user_constellation, "user_tags": rs.user_tags }, "err_str": "null"})

class get_friend_info:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        self_userid = i.self_uid
        self_token = i.token
        friend_userid = i.friend_uid
        web.header('content-type','text/json')
        if ucdb.isonline(self_userid, self_token)[0] is True:
            if ucdb.can_get_friend_info(self_userid, friend_userid) is True:
                rs = ucdb.get_user_info(friend_userid)
                if rs is None:
                    error_str = "获取好友信息失败"
                    return json.dumps({"err_code": 0, "result": {}, "err_str": error_str})
                else:
                    return json.dumps({"err_code": 1, "result": {"user_name": rs.user_name, "user_sex": rs.user_sex, "user_birthday": rs.user_birthday, "user_address": rs.user_address, "user_hobbies": rs.user_hobbies, "user_career": rs.user_career, "user_tags": rs.user_tags }, "err_str": "null"})
            else:
                error_str = "获取失败，好感度不足不能获取"
                return json.dumps({"err_code": 0, "result": {}, "err_str": error_str})
        else:
            error_str = "用户id或token错误"
            return json.dumps({"err_code": 0, "result": {}, "err_str": error_str})
            
        

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
                return json.dumps({"err_code":1, "result": rs.result[u'token'], "err_str": "null"})
            else:
                error_str = "登录失败：融云服务返回Token失败"
                return json.dumps({"err_code":0, "result": "null", "err_str": error_str})
        else:
            error_str = "用户不在线，不能重新换取token"
            return json.dumps({"err_code":0, "result": "null", "err_str": error_str})

class set_user_info:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.id
        usertoken = i.token
        username = i.user_name
        usersex = i.user_sex
        userbirthday = i.user_birthday
        useraddress = i.user_address
        userhobbies = i.user_hobbies
        usercareer = i.user_career
        usertags = i.user_tags
        web.header('Content-Type', 'text/json')
        rs = ucdb.isonline(userid, usertoken)
        if rs[0] is True:
            ucdb.set_user_info(userid, username, usersex, userbirthday, useraddress, userhobbies, usercareer, usertags)
            return json.dumps({"err_code": 1, "result": True, "err_str": "null"})
        else:
            error_str = "用户token错误，不能设置用户资料"
            return json.dumps({"err_code": 0, "result": False, "err_str": error_str})
            

class change_password_by_old_pwd:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        userid = i.id
        useroldpwd = i.oldpwd
        usernewpwd = i.newpwd
        web.header('content-type', 'text/json')
        rs = ucdb.canlogin(userid, useroldpwd)
        if rs[0] is True:
            ucdb.change_pwd(userid, usernewpwd)
            return json.dumps({"err_code": 1, "result": True, "err_str": "null"})
        else:
            error_str = "认证错误，不能修改密码"
            return json.dumps({"err_code": 0, "result": False, "err_str": error_str})


imagepath = './images'
urlpath = 'http://121.42.161.150:8080/images/'

render = web.template.render('templates/',)

class uploadimg:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.upload("")
        
    def POST(self):
        i = web.input(myfile={})
        if 'myfile' in i:
            filepath = i.myfile.filename.replace('\\','/')
            filename = filepath.split('/')[-1]
            fout =  open(imagepath + '/' + filename, 'wb')
            fout.write(i.myfile.file.read())
            fout.close()

            infile = imagepath + '/' + filename
            #outfile = infile + ".thumbnail.jpg"
            #im = Image.open(infile)
            #im.thumbnail((128, 128))
            #im.save(outfile, im.format)
        return render.upload(infile)
          
BUF_SIZE = 262144
class getimage:
    def GET(self, imgname):
        try:
            f = open(imagepath + '/' + imgname, 'rb')
            web.header('Content-type','application/octet-stream')
            web.header('Content-disposition', 'attachment; filename=%s.dat' % imgname)
            while True:
                c = f.read(BUF_SIZE)
                if c:
                    yield c
                else:
                    break;
        except Exception, e:
            print e
            yield 'Error'
        finally:
            if f:
                f.close()

if __name__=="__main__":
    app = web.application(urls, globals())
    app.run()
