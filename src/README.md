# UChatServer源文件

##源文件树:
   --base.py           //RongCouldBase,Response类<br>
   --uchatserver.py    //UChatServer类<br>
   --user.py           //User类<br>
   --uchatdb.py        //UChatDB数据库操作类<br>
   --uchatweb.py       //web接口类<br>

##程序运行
   python uchatweb.py  //开启服务器程序，通过http协议访问

###GET方式:
   http://ip:端口/register?user_id=用户ID&user_password=用户密码<br>
   http://ip:端口/login?user_id=用户ID&user_password=用户密码<br>
   http://ip:端口/logout?user_id=用户ID&token=用户保存的Token <br>
###POST方式
