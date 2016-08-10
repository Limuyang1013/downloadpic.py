#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import time
import os.path
import json

try:
    from PIL import Image
except:
    pass
from bs4 import BeautifulSoup

PWD = "D:/work/python/zhihu/"
# 构造 Request headers
# 登陆的url地址
logn_url = 'http://www.zhihu.com/#signin'

session = requests.session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
}

content = session.get(logn_url, headers=headers).content
soup = BeautifulSoup(content, 'html.parser')


def getxsrf():
    return soup.find('input', attrs={'name': "_xsrf"})['value']


# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, allow_redirects=False).status_code
    if int(x=login_code) == 200:
        return True
    else:
        return False


def login(secret, account):
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': getxsrf(),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
    else:
        print("邮箱登录 \n")
        post_url = 'http://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': getxsrf(),
            'password': secret,
            'remember_me': 'true',
            'email': account,
        }
    try:
        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.text
        print(login_page.status)
        print(login_code)
    except:
        # 需要输入验证码后才能登录成功
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = eval(login_page.text)
        print(login_code['msg'])


def downpic(filename, url):
    print("正在下载 " + url)
    try:
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)
    except Exception as e:
        print("下载失败了", e)


# def gettitle():
#     question_url = 'https://www.zhihu.com/question/37709992'
#     question_header = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
#     question = session.get(question_url, headers=question_header)
#     question_soup = BeautifulSoup(question.content, 'html.parser')
#     print(question_soup.title.text)
#     count = 0
#     photoNum = 1
#     pattern = re.compile('<a class="author-link".*?<span title=.*?<div class="zh-summary.*?' +
#                          '<div class="zm-editable-content.*?>(.*?)</div>', re.S)
#     items = re.findall(pattern, question.text)
#     imagesurl = []
#     pattern = re.compile('data-actualsrc="(.*?)">', re.S)
#     for item in items:
#         urls = re.findall(pattern, item)
#         imagesurl.extend(urls)
#     for url in imagesurl:
#         myurl = url
#         filename = PWD + str(count) + '.jpg'
#         if os.path.isfile(filename):
#             print("文件存在：", filename)
#             count += 1
#             continue
#         else:
#             downpic(filename, myurl)
#         count += 1
#         photoNum += 1
#     # for author in question_soup.findAll('a', attrs={'class': 'author-link'}):
#     # print("=======正在下载" + author.text + "的照片======")
#     # filename = PWD + str(author.text) + str(count) + '.jpg'
#     print("一共下载了{0} 张照片".format(photoNum))


def change(offset, count, photoNum):
    url = 'https://www.zhihu.com/node/QuestionAnswerListV2'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Referer': 'https://www.zhihu.com/question/37709992',
        'Origin': 'https://www.zhihu.com',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    data = {
        'method': 'next',
        'params': '{"url_token":' + str(37709992) + ',"pagesize": "10",' + \
                  '"offset":' + str(offset) + "}",
        '_xsrf': getxsrf(),

    }
    try:
        question = session.post(url, headers=header, data=data)
        offset += 1
        dic = json.loads(question.content.decode('ISO-8859-1'))
        li = dic['msg'][0]
        pattern = re.compile('<a class="author-link".*?<span title=.*?<div class="zh-summary.*?' +
                             '<div class="zm-editable-content.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, li)
        imagesurl = []
        pattern = re.compile('data-actualsrc="(.*?)">', re.S)
        for item in items:
            urls = re.findall(pattern, item)
            imagesurl.extend(urls)
        for url in imagesurl:
            myurl = url
            filename = PWD + str(count) + '.jpg'
            if os.path.isfile(filename):
                print("文件存在：", filename)
                count += 1
                continue
            else:
                downpic(filename, myurl)
                count += 1
                photoNum += 1
            print("一共下载了{0} 张照片".format(photoNum))
            if not os.path.exists(PWD):
                os.makedirs(PWD)
        change(offset, count, photoNum)
    except:
        print("下载出错")


if __name__ == '__main__':

    if isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名\n>  ')
        secret = input("请输入你的密码\n>  ")
        login(secret, account)
    change(offset=0, count=0, photoNum=0)
