dzimport requests
import time
import json
import csv
import random
from bs4 import BeautifulSoup
import re
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

"""
本项目首发：
B站原创视频：https://www.bilibili.com/video/BV1Vz41187Rt
公众号原创文章：https://mp.weixin.qq.com/s/fVDwNdVDZo_0q6jAMWCGAA
公众号：Python知识圈（id：PythonCircle）
哔哩哔哩：菜鸟程序员的日常
"""


def request_data():
    article_url_list = []
    print('正在下载，请稍等！大约需要30分钟')
    for offset in range(0, 310, 10):
        # 记得把offset后面的值改成{}
        base_url = 'http://mp.weixin.qq.com/mp/profile_ext?offset={}&count=10'

        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行
        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行
        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行

        cookies = {
        'rewardsn': '',
        'wxtokenkey': '777',
        'wxuin': '440549995',
        'devicetype': 'iPhoneiOS13.5',
        'version': '17000c30',
        'lang': 'zh_CN',
        'pass_ticket': 'HqWmXzmNr8KpFJFQ6tJcCBSY6ZFptPPRlNZDhVACMW7M03uOUDFzS2t2gL4xbkV5',
        'wap_sid2': 'COuEidIBElxDdEsxT1d3WDUxOV85Um1KcmNMdTVUekNmaE1vd3JGcC1WVTdKajl0WDFCejJ1VmF0MEs3YjlWdFpsMDAtSUcyRjJGandndnlKSktRTExNZW00RThvaWdFQUFBfjDo/fb2BTgNQJVO', 
        }

        headers = {
        'Host': 'mp.weixin.qq.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
        'x-requested-with': 'XMLHttpRequest',
        'accept': '*/*',
        'referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI5MTE2NDI2OQ==&scene=124&uin=NDQwNTQ5OTk1&key=fda40951308f13b025b34c83e2da4024a0bc0bbf21b4067435859f027f00cd836cf6178834dcbf2f07998d37d7fa125bdbb73fe32ae7f0050977fb7daa543e31e6e47850613593cc901fefc676a22881&devicetype=Windows+10+x64&version=62090070&lang=zh_CN&a8scene=7&pass_ticket=HqWmXzmNr8KpFJFQ6tJcCBSY6ZFptPPRlNZDhVACMW7M03uOUDFzS2t2gL4xbkV5&winzoom=1',
        'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
        }

        params = (
        ('action', 'getmsg'),
        ('__biz', 'MzI5MTE2NDI2OQ=='),
        ('f', ['json', 'json']),
        ('is_ok', '1'),
        ('scene', '124'),
        ('uin', 'NDQwNTQ5OTk1'),
        ('key', 'fda40951308f13b025b34c83e2da4024a0bc0bbf21b4067435859f027f00cd836cf6178834dcbf2f07998d37d7fa125bdbb73fe32ae7f0050977fb7daa543e31e6e47850613593cc901fefc676a22881'),
        ('pass_ticket', 'HqWmXzmNr8KpFJFQ6tJcCBSY6ZFptPPRlNZDhVACMW7M03uOUDFzS2t2gL4xbkV5'),
        ('wxtoken', ''),
        ('appmsg_token', '1064_HThtm5x1N3uLWJSpTsEk1Ycd40pTaws-QLm2og~~'),
        ('x5', '0'),
        )

        # 代理ip，失效的话请自行更换，也可以直接去掉
        proxy = {'https': '223.247.95.106:4216'}

        try:
            response = requests.get(
                base_url.format(offset),
                headers=headers,
                params=params,
                cookies=cookies,
                proxies=proxy)
            if 200 == response.status_code:
                all_datas = json.loads(response.text)
                if 0 == all_datas['ret'] and all_datas['msg_count'] > 0:
                    summy_datas = all_datas['general_msg_list']
                    datas = json.loads(summy_datas)['list']
                    for data in datas:
                        try:
                            article_url = data['app_msg_ext_info']['content_url']
                            article_url_list.append(article_url)
                        except Exception as e:
                            continue
        except:
            time.sleep(2)
        time.sleep(int(format(random.randint(2, 5))))
    return article_url_list


def get_urls(url):
    try:
        html = requests.get(url, timeout=30).text
    except requests.exceptions.SSLError:
        html = requests.get(url, verify=False, timeout=30).text
    except TimeoutError:
        print('请求超时')
    except Exception:
        print('获取失败')
    src = re.compile(r'data-src="(.*?)"')
    urls = re.findall(src, html)
    if urls is not None:
        url_list = []
        for url in urls:
            url_list.append(url)
        return url_list


def mkdir():
    isExists = os.path.exists(r'./banfo')
    if not isExists:
        print('创建目录')
        os.makedirs(r'./banfo')  # 创建目录
        os.chdir(r'./banfo')  # 切换到创建的文件夹
        return True
    else:
        print('目录已存在，即将保存！')
        return False


def download(filename, url):
    try:
        with open(filename, 'wb+') as f:
            try:
                f.write(requests.get(url, timeout=30).content)
                print('成功下载图片：', filename)
            except requests.exceptions.SSLError:
                f.write(requests.get(url, verify=False, timeout=30).content)
                print('成功下载图片：', filename)
    except FileNotFoundError:
        print('下载失败，非表情包，直接忽略：', filename)
    except TimeoutError:
        print('下载超时：', filename)
    except Exception:
        print('下载失败：', filename)

"""
本项目首发：
B站原创视频：https://www.bilibili.com/video/BV1Vz41187Rt
公众号原创文章：https://mp.weixin.qq.com/s/fVDwNdVDZo_0q6jAMWCGAA
公众号：Python知识圈（id：PythonCircle）
哔哩哔哩：菜鸟程序员的日常
"""
        
if __name__ == '__main__':
    for url in request_data():
        url_list = get_urls(url)
        mkdir()
        for pic_url in url_list:
            filename = r'./banfo/' + pic_url.split('/')[-2] + '.' + pic_url.split('=')[-1]   # 图片的路径
            download(filename, pic_url)

            
            
