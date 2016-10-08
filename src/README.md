# UChatServer源文件

##源文件树:
   --base.py           //RongCouldBase,Response类<br>
   --uchatserver.py    //UChatServer类<br>
   --user.py           //User类<br>
   --uchatdb.py        //UChatDB数据库操作类<br>
   --uchatweb.py       //web接口类<br>

##程序运行
   python uchatweb.py  //开启服务器程序，通过http协议访问

###GET方式
   http://ip:端口/uploadimg

###POST方式
   所有POST接口一律返回json数据类型

   http://ip:端口/register
   参数: id
         pwd

   http://ip:端口/login
   参数: id
         pwd

   http://ip:端口/logout
   参数: id
         token

   http://ip:端口/reconnect
   参数: id
         token

   http://ip:端口/get_self_info
   参数: id
         token

   http://ip:端口/get_friend_info
   参数: self_uid
         token
         friend_uid
         
