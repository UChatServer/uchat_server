#uchat server

##安装python2.7
##安装python-devel包
    sudo yum install python-devel
    sudo yum install zlib-devel
    sudo yum install libjpeg-turbo-devel

##安装pip
    --pip install requests
    --pip install MySQL-python

    --pip install image (CentOS需要libjpeg-turbo-devel)

##安装web.py
    wget http://webpy.org/static/web.py-0.38.tar.gz
    或者使用uchat/third_party/下的web.py-0.38.tar.gz
    <br>
    tar -xvf web.py-0.38.tar.gz
    cd web.py-0.38
    python setup.py install   (需要root权限)
    
安装mysql
 
