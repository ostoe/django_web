from django.test import TestCase
from blog.models import Users, Comments, Blogs
import uuid, time
# Create your tests here.


def test1(name, email, passwd):
    result = Users.objects.filter(email=email).first()
    res = Users.objects.all()
    print(res, result.email)
    # Users.objects.create(id = next_id(), name=name, email=email,
    #                      admin=1, passwd=passwd, created_at=time.time())

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

# def test(title, abstract, content):
#     Blogs.objects.create(id=next_id(), user_id='abdd',
#                          user_name='fff',
#                          title=title, content=content, abstract=abstract,
#                          created_at=time.time())


def test(name, blog_id, user_id, content):
    Comments.objects.create(
    id = next_id(),
    blog_id = blog_id,
    user_id = user_id,
    user_name = name,
    content = content,
    created_at = time.time(),
    )
name = 'abcd'
email = '1131562995@qq.com'
passwd = '123456'
title = "吃"
abstract = "哈哈哈哈"
content = "方式发送方哥哥"
# test(name, email, passwd)
test(name, 'ffff', 'fsfaffg', content)