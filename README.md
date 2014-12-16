auto_install
============

自动装机系统，可以配置ILO，RAID,通过PXE启动，自动发现机器添加到装机系统中，目前执行机型，DELL,IBM,浪潮，华为 ,HP
-----------------
依赖组件
*   python 1.7+
*   Django 1.7
*   request
*   python-memcached
*   mysql-python

------------------
目录结构

        auto_install/
        ├── auto_install
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        ├── conf_file
        ├── manage.py
        ├── pxe
        │   ├── admin.py
        │   ├── forms.py
        │   ├── __init__.py
        │   ├── models.py
        │   ├── tests.py
        │   └── views.py
        ├── static
        │   ├── boot
        │   │   ├── css
        │   │   │   ├── bootstrap.css
        │   │   │   ├── bootstrap.min.css
        │   │   │   ├── bootstrap-theme.css
        │   │   │   ├── bootstrap-theme.min.css
        │   │   │   ├── scojs.css
        │   │   │   └── sco.message.css
        │   │   ├── fonts
        │   │   └── js
        │   │       ├── ajax.js
        │   │       ├── bootstrap.js
        │   │       ├── bootstrap.min.js
        │   │       ├── jquery.js
        │   │       ├── npm.js
        │   │       ├── sco.confirm.js
        │   │       ├── sco.modal.js
        │   │       └── sco.valid.js
        │   └── images
        ├── templates
        │   ├── base.html
        │   ├── edit.html
        │   ├── exe.html
        │   ├── find.html
        │   ├── his.html
        │   ├── info.html
        │   ├── install.html
        │   ├── ks
        │   │   ├── conf.cfg
        │   │   └── webserver.cfg
        │   └── login.html
        └── tools
            ├── auto_install.sh
            ├── index.py
            └── post.sh
![截图](https://raw.githubusercontent.com/gaoming655/auto_install/master/static/images/jt_login.jpg) 

![截图](https://raw.githubusercontent.com/gaoming655/auto_install/master/static/images/jt.jpg)  

![截图](https://raw.githubusercontent.com/gaoming655/auto_install/master/static/images/info.jpg)  

![截图](https://raw.githubusercontent.com/gaoming655/auto_install/master/static/images/edit.jpg) 

![截图](https://raw.githubusercontent.com/gaoming655/auto_install/master/static/images/jd.jpg)

![截图](https://raw.githubusercontent.com/gaoming655/auto_install/master/static/images/wancheng.jpg)
