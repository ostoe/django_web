# django_web
# 使用django + uwsgi + nginx开发部署的blog网站

### 网址为：https://ostoe.eu.org/

![img](static/img/md-1.png)

#### Done---> 主页显示
#### Done---> 创建blog；显示blog；加入头像(头像目前随机储存在本地)
#### Done---> 用户注册，登录


先运行
python prexxx.py 拉取图片；

```bash
 # ref: https://docs.djangoproject.com/zh-hans/4.1/topics/migrations/
python manage.py makemigrations

python manage.py migrate

# 运行项目 
python manage.py runserver

# 指定端口运行项目
python manage.py runserver 8080

# 指定端口IP运行项目
python manage.py runserver 0.0.0.0:8080
```