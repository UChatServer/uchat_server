#python
# coding:utf8
import sys
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
ucdb = UChatDB(dbname = 'uchat', username = 'uchat', password = 'uchat', host = '47.88.23.214')

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
    '/set_location', 'set_location',
    '/get_recommend_friends', 'get_recommend_friends',
    '/get_friend_list', 'get_friend_list',
    '/add_friend', 'add_friend',
    '/del_friend', 'del_friend',
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
        try:
            i = web.input()
            userid = i.id
            password = i.pwd
            name = i.name
            birthday = i.birthday
            sex = i.sex
        except Exception,e:
            error_str =  "参数异常"
            print error_str
            return json.dumps({"err_code":0, "result":False, "err_str": error_str})
        web.header('content-type','text/json')
        rs = ucdb.register(userid, password, name, birthday, sex)
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
            return json.dumps({"err_code": 1, "result": {"user_name": rs.user_name, "user_sex": rs.user_sex, "user_birthday": rs.user_birthday, "user_address": rs.user_address, "user_hobbies": rs.user_hobbies, "user_career": rs.user_career, "user_tags": rs.user_tags }, "err_str": "null"})

class get_friend_info:
    def POST(self):
        global ucs
        global ucdb
        i = web.input()
        self_userid = i.id
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

class get_friend_list:
    def POST(self):
        global ucs
        global ucdb
        web.header('content-type', 'text/json')
        try:
            i = web.input()
            uid = i.id
            utoken = i.token
            ofst = i.offset
            lmt = i.limit
        except Exception, e:
            print "get_friend_list 参数异常"
            return json.dumps({"err_code":0, "result": [], "err_str": "参数错误"})
        rs = ucdb.get_friends(uid, utoken, ofst, lmt)
        if rs[0] is True:
            return json.dumps({"err_code": 1, "result": rs, "err_str": "null"})
        else:
            return json.dumps({"err_code": 0, "result": [], "err_str": rs[1]})
           

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
        web.header('content-type', 'text/json')
        i = web.input()
        
        flag = True
        userid = i.get("id")
        if userid is None:
            flag = False
        usertoken = i.get("token")
        if usertoken is None:
            flag = False
        if flag is False:
            return json.dumps({"err_code": 0, "result": False, "err_str": "参数获取错误"})


	datamap = {}
        username = i.get("name")
        if username is not None:
            datamap["user_name"] = username
        usersex = i.get("sex")
        if usersex is not None:
            datamap["user_sex"] = usersex
        userbirthday = i.get("birthday")
        if userbirthday is not None:
            datamap["user_birthday"] = userbirthday
        userprovince = i.get("privince")
        if userprovince is not None:
            datamap["user_province"] = userprovince
        usercity = i.get("city")
        if usercity is not None:
            datamap["user_city"] = usercity
        userhobbies = i.get("hobbies")
        if userhobbies is not None:
            datamap["user_hobbies"] = userhobbies
        usercareer = i.get("career")
        if usercareer is not None:
            datamap["user_career"] = usercareer
        userconstellation = i.get("constell")
        if userconstellation is not None:
            datamap["user_constellation"] = userconstellation
        usertags = i.get("tags")
        if usertags is not None:
            datamap["user_tags"] = usertags
        rs = ucdb.isonline(userid, usertoken)
        if rs[0] is True:
            ucdb.set_user_info(userid, datamap)
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


imagepath = '/home/kongyt/uchat_server/src/images'
urlpath = 'http://www.kongyt.com/images/'

render = web.template.render('/home/kongyt/uchat_server/src/templates/',)

class uploadimg:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.upload("")
        
    def POST(self):
        i = web.input(myfile={})
        if 'myfile' in i:
            filepath = i.myfile.filename.replace('\\','/')
            filename = filepath.split('/')[-1]
            fout =  open(imagepath + '/' + filename, 'wb+')
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


class set_location:
    def POST(self):
        i = web.input()
        userid = i.get("id")
	if userid is None:
            return json.dumps({"err_code": 0, "result": False, "err_str": "参数错误:没有获取到id值"})
        usertoken = i.get("token")
        if usertoken is None:
            return json.dumps({"err_code": 0, "result": False, "err_str": "参数错误:没有获取到token值"})
        userlongitude = i.get("longitude")
        if userlongitude is None:
            return json.dumps({"err_code": 0, "result": False, "err_str": "参数错误:没有获取到longitude值"})
        userlatitude = i.get("latitude")
        if userlatitude is None:
            return json.dumps({"err_code": 0, "result": False, "err_str": "参数错误:没有获取到latitude值"})
        datamap = {}
        datamap["user_longitude"] = userlongitude
        datamap["user_latitude"] = userlatitude
        web.header('Content-Type', 'text/json')
        rs = ucdb.isonline(userid, usertoken)
        if rs[0] is True:
            ucdb.set_user_info(userid, datamap)
            return json.dumps({"err_code": 1, "result": True, "err_str": "null"})
        else:
            error_str = "用户token错误，不能设置用户位置"
            return json.dumps({"err_code": 0, "result": False, "err_str": error_str})


class get_recommend_friends:
    def POST(self):
        global ucs
        global ucdb
        web.header('content-type', 'text/json')
        try:
            i = web.input()
            userid = i.id
            usertoken = i.token
            ofst = i.page * 10
            lmt = 10
        except Exception,e:
            return json.dumps({"err_code": 0, "result": [], "err_str": "参数异常"})
        rs =  ucdb.get_recommend_friends(userid, usertoken, ofst, lmt)
        if rs[0] is True:
            return json.dumps({"err_code": 1, "result": rs[1], "err_str": "null"})
        else:
            return json.dumps({"err_code": 0, "result": [], "err_str": rs[1]})
  

class add_friend:
    def POST(self):
        global ucs
        global ucdb
        web.header('content-type', 'text/json')
        try:
            i = web.input()
            userid = i.id
            utoken = i.token
            userid2 = i.id2
        except Exception,e:
            return json.dumps({"err_code": 0, "result": False, "err_str": "参数异常"})
        rs = ucdb.add_friend(userid, token, userid2)
        if rs[0] is True:
            return json.dumps({"err_code": 1, "result": True, "err_str": "null"})
        else:
            return json.dumps({"err_code": 0, "result": False, "err_str": rs[1]})
class del_friend:
     def POST(self):
        global ucs
        global ucdb
        web.header('content-type', 'text/json')
        try:
            i = web.input()
            userid = i.id
            utoken = i.token
            userid2 = i.id2
        except Exception,e:
            return json.dumps({"err_code": 0, "result": False, "err_str": "参数异常"})
        rs = ucdb.del_friend(userid, token, userid2)
        if rs[0] is True:
            return json.dumps({"err_code": 1, "result": True, "err_str": "null"})
        else:
            return json.dumps({"err_code": 0, "result": False, "err_str": rs[1]})

def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write( "fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    os.chdir('/')
    os.umask(0)
    os.setsid()

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" %(e.errno, e.strerror))
        sys.exit(1)

    for f in sys.stdout, sys.stderr:
        f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


if __name__=="__main__":
    daemonize('/dev/null', '/tmp/daemon_stdout.log', '/tmp/daemon_error.log')
    app = web.application(urls, globals())
    app.run()
