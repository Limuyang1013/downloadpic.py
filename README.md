# DownloadPic
下载知乎某个回答下的所有图片

亲测如果需要下载另一个问题的答案，只需要在:
```
 data = {
        'method': 'next',
        'params': '{"url_token":' + str(37709992) + ',"pagesize": "10",' + \
                  '"offset":' + str(offset) + "}",
        '_xsrf': getxsrf(),

    }
```
更换那串数字就行，就好比这样的形式：
> https://www.zhihu.com/question/48720845

但是这种形式的把数字换上去不起效：

> https://www.zhihu.com/question/49078894#answer-41776282

这个好像是知乎热门问答的链接形式，暂时没有深究
