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
   参数: id
         token
         friend_uid

   http://ip:端口/set_user_info
   参数: id
         token
   可选参数:
         name
         sex
         birthday
         address
         hobbies
         career
         tags 

   http://ip:端口/change_password_by_old_pwd
   参数: id
         oldpwd
         newpwd

   http://ip:端口/set_location
   参数: id
         token
         longitude
         latitude

   http://ip:端口/get_recommend_friends
   参数: id
         token
         page
   可选参数:(暂不支持)
         sex
         age
         distance
         province
         city
         career
         hobbies     


   http://ip:端口/add_friend
   参数: id
         token
         id2
 
   http://ip:端口/del_friend
   参数: id
         token
         id2

   http://ip:端口/get_friend_list
   参数: id
         token
         offset
         limit   
