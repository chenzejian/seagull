## 安装步骤


### 1：下载项目代码

```git 
git clone git@git.umlife.net:chenzejian/ym-email.git
```

### 2：创建一个虚拟环境

```virtualenv
pip install virtualenv
cd /path/to/project
virtualenv -p /usr/bin/python3.5 venv　　#使用python3.5,venv为虚拟环境目录名，目录名自定义
```
推荐使用virtualenv管理工具virtualenvwrapper

### 3：安装项目依赖

```pip
pip install -r requirements.txt
```


### 4：复制并修改本地配置环境文件

```config
cp config/settings.py.demo config/settings.py
cp config/celeryconfig.py.demo config/celeryconfig.py
```
修改配置文件，如数据库配置,邮件配置等

### 5：初始化数据库及管理后台的超级用户（已有数据库这步直接跳过）

```shell
python manage.py migrate
python manage.py runscript sync_database
python manage.py createsuperuser
```

### 6：运行服务

```shell
python manage.py runserver
celery -A app worker --loglevel=info
```

### 7: 测试接口

```api
POST http://localhost:8000/api/send_email
```

### 8: 在浏览器打开管理后台 http://localhost:8000/admin



