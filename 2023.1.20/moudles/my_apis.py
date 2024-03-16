import requests
import random
from flask import Flask,request
from datetime import datetime
from lxml import etree
app = Flask(__name__)

'''
漂流瓶功能
接口链接为127.0.0.1:5000/bottle?qq=QQ号&group=群号&type=1&msg=消息内容
注：
必填参数：qq号--即触发关键词用户qq号
        群号--即触发关键词用户所在群号
可选参数：type--扔瓶子则为1，捡瓶子时可省略或为空
        msg--扔瓶子的瓶子内容，捡瓶子时可省略为空
返回：字符串--操作完成后相关提示消息
'''


@app.route('/bottle')
def bottle():
    type = request.args.get('type')
    qq = request.args.get('qq')
    group = request.args.get('group')
    msg = request.args.get('msg')
    if type == '1':
        if msg:
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('bottles.txt','a')as f:
                f.write(f'恭喜你捞到了{qq}的瓶子，来自群{group}，留言时间{date_time}，小纸条内容如下：{msg}\n')
            response = '保存成功，您的瓶子已飘向远方。'
        else:
            response = '请不要随便扔空瓶子，让捡到的人寂寞流泪。'
    else:
        try:
            with open('bottles.txt', 'r') as f:
                data = f.readlines()
                random_bottle = random.choice(data)
                response = random_bottle
        except FileNotFoundError:
            response = '目前没有在外的漂流瓶。'
    return response


'''
随机图片功能
接口链接为127.0.0.1:5000/picture?q=搜索内容
注：
必填参数：q--即随机图片的内容
返回：字符串--图片url链接
'''


@app.route('/picture')
def picture():
    msg = request.args.get('q')
    url = f'https://cn.bing.com/images/search?q={msg}'
    data = etree.HTML(requests.get(url).text)
    response = data.xpath('//div[@class="imgpt"]/a/@href')
    img_url = 'https://cn.bing.com' + random.choice(response)
    return img_url

if __name__ == '__main__':
    app.run()