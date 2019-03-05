from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from blog.models import Users, Comments, Blogs
import json
import random, time, uuid
from datetime import datetime
from django.views.decorators.cache import cache_page
import string
import functools
import glob

# Create your views here.

characters = string.ascii_letters


# user_list = [
#     {"user": "jack", "pwd": "abc"},
#     {"user": "tom", "pwd": "ABC"},
# ]

def cookie_auth(func):
    @functools.wraps(func)
    def weaper(request, *args, **kwargs):
        logined = {'login': False, 'headimg':'/static/img/client2.jpg'}
        # request.session.flush()
        request.session.clear_expired()
        v = request.session.get('email', None)
        if v is not None:
            obj = Users.objects.filter(email=v).first()
            logined = {'login': True, 'email': v, 'headimg':obj.head_img.url}
        return func(request, *args, **logined, **kwargs)

    return weaper


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return '1分钟前'
    if delta < 3600:
        return '%s分钟前' % (delta // 60)
    if delta < 86400:
        return '%s小时前' % (delta // 3600)
    if delta < 604800:
        return '%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return '%s:%s:%s' % (dt.year, dt.month, dt.day)


def obj_dic(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dic(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                    type(j)(obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top


# @cache_page(60 * 15)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
@cookie_auth
def index(request, *args, **kwargs):
    blogs = Blogs.objects.all()

    return render(request, 'index.html', {"data": 'blogs', '__user__': {'login': kwargs['login'],'headimg': kwargs['headimg']}})


# def add2(request, a, b):
#     c = int(a) + int(b)
#     return HttpResponse(str(c))

@cookie_auth
def muti_blogs(request, *args, **kwargs):
    # logined = kwargs.get('logined')
    content = '喝茶当于瓦屋纸窗之下，清泉绿茶，用素雅陶瓷茶具，同二三人同饮，得半日之闲，可抵十年尘梦。'
    blogs = []
    """QuerySet 支持切片 Entry.objects.all()[:10] 取出10条，可以节省内存;用 len(es) 
    可以得到Entry的数量，但是推荐用 Entry.objects.count()来查询数量，后者用的是SQL：SELECT COUNT(*)"""
    blogs_nb = Blogs.objects.count()
    result = Blogs.objects.all().order_by('-created_at')[:blogs_nb]

    for i, x in enumerate(result):
        blog = {}
        blog['id'] = x.id
        blog['title'] = x.title
        blog['author'] = x.user_name
        blog['content'] = x.content
        blog['datetime'] = datetime_filter(x.created_at)
        blog['image'] = x.user_image.url
        blog['abstract'] = x.abstract

        comments_nb = Comments.objects.filter(blog_id=x.id).count()
        # print(comments_nb)
        blog['comments'] = comments_nb
        blogs.append(blog)
    # l = [{'title':'title', 'content':content, 'date':'12:30pm', 'random':'1'}]
    return render(request, 'blogs.html', {'__user__': {'login': kwargs['login'], 'headimg': kwargs['headimg']}, 'blogs': blogs})


# single blog
@cookie_auth
def single_blog(request, *args, **kwargs):
    if request.method == 'GET':
        result = Blogs.objects.get(id=kwargs['blog_id'])

        # blog
        comments = []
        blog = {}
        obj = Users.objects.filter(id=result.user_id)
        if len(obj) == 0:
            blog['authorimg']  = "https://api.berryapi.net/bing/random/?561/400"
        else:
            blog['authorimg'] = obj.first().head_img.url
        # blog['id'] = x.id
        blog['title'] = result.title
        blog['author'] = result.user_name
        blog['content'] = result.content
        blog['datetime'] = datetime_filter(result.created_at)
        blog['image'] = result.user_image.url
        blog['abstract'] = result.abstract
        blog['totoal_posts'] = Blogs.objects.filter(user_id=result.user_id).count()


        comments_result = Comments.objects.filter(blog_id=kwargs['blog_id'])
        blog['comments'] = comments_result.count()

        # comments

        order_comments = comments_result.order_by('-created_at')
        for x in order_comments:
            obj = Users.objects.filter(id=x.user_id)
            if obj.count() != 0:
                headimg = obj.first().head_img.url
            else:
                headimg = "https://api.berryapi.net/bing/random/?560/400"
            comment = {}
            comment['name'] = x.user_name
            comment['content'] = x.content
            comment['datetime'] = datetime_filter(x.created_at)
            comment['headimg'] = headimg
            comments.append(comment)

        return render(request, 'single_blog.html',
                      {'blog': blog, 'comments': comments, '__user__': {'login': kwargs['login'], 'headimg': kwargs['headimg']}
                       })
    else:
        # print(request.POST)
        comment = request.POST.get('comment')
        if kwargs['login']:
            result = Users.objects.get(email=kwargs['email'])
            user_id = result.id
            user_name = result.name
        else:
            user_id = next_id()
            user_name = ''.join(random.choices(characters, k=8))
        Comments.objects.create(
            id=next_id(),
            blog_id=kwargs['blog_id'],
            user_id=user_id,
            user_name=user_name,
            content=comment,
            created_at=time.time(),
        )

        return HttpResponseRedirect('/blog/%s' % kwargs['blog_id'])


# register
def register(request, *args, **kwargs):
    logined = {'login': False}
    if request.method == 'GET':
        return render(request, 'register.html', {"data": 'blogs', '__user__': logined})
    # __user__ = {'login': False}
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    passwd = request.POST.get('passwd', None)

    user_nb = Users.objects.filter(email=email).count()
    if user_nb == 0:
        image_list = glob.glob('static/img/headimgs/*.jpg')
        image_path = random.choice(image_list)

        d = {'status': True}
        Users.objects.create(id=next_id(), name=name, email=email,
                             admin=1, passwd=passwd, created_at=time.time())
        with open(image_path, 'rb') as fp:
            Users.objects.filter(email=email).first().head_img.save(image_path.split('/')[-1], fp)
        request.session['name'] = email
        request.session['email'] = email
    else:
        d = {'status': False}

    # # 更新所有头像
    # image_list = glob.glob('static/img/headimgs/*.jpg')
    # for x in Users.objects.all():
    #     image_path = random.choice(image_list)
    #     with open(image_path, 'rb') as fp:
    #         x.head_img.save(image_path.split('/')[-1], fp)
    # result = Users.objects.get(email=email)
    return HttpResponse(json.dumps(d), content_type="application/json")


# signin
@cookie_auth
def signin(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['login']:
            return redirect('/')
        else:
            return render(request, 'signin.html', {"data": 'blogs', '__user__': {'login': kwargs['login']}})
    email = request.POST.get('email', None)
    passwd = request.POST.get('passwd', None)
    result = Users.objects.filter(email=email).first()
    if result is None:
        d = {'status': 'email not exist!'}
        # result = Users.objects.get(email=email)
    elif passwd == result.passwd:
        # cookie
        request.session['name'] = result.name
        request.session['email'] = result.email
        # request.session.flush()
        d = {'status': 'well'}
    else:
        d = {'status': 'incrrect password'}

    return HttpResponse(json.dumps(d), content_type="application/json")


# signout
def signout(request, *args, **kwargs):
    # request.session.clear()
    request.session.flush()
    return HttpResponseRedirect('/')


# 全局登录的装饰器

# write blog
@cookie_auth
def write_blog(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'create_blog.html', {'__user__': {'login': kwargs['login'], 'headimg': kwargs['headimg']}})

    title = request.POST.get('title', None)
    abstract = request.POST.get('abstract', None)
    content = request.POST.get('content', None)

    v = request.session.get('email', None)
    # print(v, type(v))
    if v:
        result = Users.objects.filter(email=v).first()
        user_id = result.id
        user_name = result.name
    else:
        user_id = next_id()
        user_name = ''.join(random.choices(characters, k=8))
    image_list = glob.glob('static/img/blogimgs/*.jpg')
    image_path = random.choice(image_list)

    id = next_id()
    Blogs.objects.create(id=id, user_id=user_id,
                         user_name=user_name,
                         title=title,
                         content=content,
                         abstract=abstract,
                         # user_image = img,
                         created_at=time.time())

    with open(image_path, 'rb') as fp:
        Blogs.objects.filter(id=id).first().user_image.save(image_path.split('/')[-1], fp)
    # list1 = Blogs.objects.all() #更新所有blog图片
    # for obj in list1:
    #     image_path = random.choice(image_list)
    #     with open(image_path, 'rb') as fp:
    #         obj.user_image.save(image_path.split('/')[-1], fp)
    d = {'status': 'well'}
    return HttpResponse(json.dumps(d), content_type="application/json")
