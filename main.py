#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/24 13:04
# @Author  : lockcy
# @File    : main.py


import requests
import json
import configparser
<<<<<<< HEAD
=======
import re
from logger import logger
from apscheduler.schedulers.blocking import BlockingScheduler
>>>>>>> 20210328

r = requests.session()

PROXY = {'http': '127.0.0.1:8080'}

f = configparser.RawConfigParser()
f.read('config.ini')

<<<<<<< HEAD
ACF_AUTH = f.get("cookies",  "ACF_AUTH")
CTN = f.get("cookies", "CTN")

# 获取背包小礼物
def get_backpack():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Referer": "https://www.douyu.com/",
    }
    cookies = {
        "acf_auth": ACF_AUTH,
    }
    html = r.get(url='https://www.douyu.com/japi/prop/backpack/web/v1?rid=957090', headers=header, cookies=cookies)

    info_json = json.loads(html.text)
    gift_json = info_json.get('data').get('list')
    if gift_json:
        for item in gift_json:
            print('小礼物id: ', item.get('id'))
            print('小礼物名称: ', item.get('name'))
            print('小礼物数量: ', item.get('count'))
            print('小礼物过期天数: ', item.get('expiry'))
    else:
        print('获取背包信息失败')

# 赠送礼物接口propid:小礼物id propcount:赠送小礼物数量  roomid:房间号
def send_gift(propid, propcount, roomid):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Referer": "https://www.douyu.com/",
    }
    cookies = {
        "acf_auth": ACF_AUTH,
    }
    datas = {
        'propId': propid,
        'propCount': propcount,
        'roomId': roomid,
        'bizExt': '{"yzxq":{}}',
    }
    html = r.post(url='https://www.douyu.com/japi/prop/donate/mainsite/v1', headers=header, cookies=cookies, data=datas)
    info_json = json.loads(html.text)
    gift_json = info_json.get('data').get('list')
    if gift_json:
        print('赠送小礼物成功')
    else:
        print('赠送小礼物失败')


# 签到这里有个坑,签到后前端的签到按钮不会改变（实际上已经签到）
def check_in(roomId):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Referer": "https://www.douyu.com/",
    }
    cookies = {
        "acf_auth": ACF_AUTH,
        "acf_ccn": CTN,
    }
    datas = {
        'rid': roomId,
        'ctn': CTN
    }
    html = r.post(url="https://www.douyu.com/japi/roomuserlevel/apinc/checkIn", headers=header, cookies=cookies, data=datas)
    print(html.text)
=======
# 先初步设定有粉丝牌的房间每天定时刷20个荧光棒
def set_task():
    douyu = Douyu()
    # 定时查询关注的房间(开播中)，并签到
    lives = douyu.get_live_room()
    for live in lives:
        douyu.check_in(live)
    # 定时给有粉丝牌的房间刷小礼物
    fans = douyu.get_fans_rid()
    for fan in fans:
        douyu.send_gift(268, 20, fan)



class Douyu(object):
    def __init__(self):
        f = configparser.RawConfigParser()
        f.read('config.ini')
        self.acf_auth = f.get("cookies", "ACF_AUTH")
        self.ctn = f.get("cookies", "CTN")

        self.header ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Referer": "https://www.douyu.com/",
        }
    # 获取背包小礼物
    def get_backpack(self):
        cookies = {
            "acf_auth": self.acf_auth,
        }
        html = r.get(url='https://www.douyu.com/japi/prop/backpack/web/v1?rid=957090', headers=self.header, cookies=cookies)
        info_json = json.loads(html.text)
        gift_json = info_json.get('data').get('list')
        if gift_json:
            logger.info('获取背包信息成功')
            for item in gift_json:
                info = '小礼物id: ' + str(item.get('id'))
                info = info + ' 小礼物名称: ' + str(item.get('name'))
                info = info + ' 小礼物数量: ' + str(item.get('count'))
                info = info + ' 小礼物过期天数: ' + str(item.get('expiry'))
                logger.info(info)
        elif info_json.get('msg') == 'success':
            logger.info('背包为空')
        else:
            logger.info('获取背包信息失败')

    # 赠送礼物接口propid:小礼物id propcount:赠送小礼物数量  roomid:房间号
    def send_gift(self, propid, propcount, roomid):
        cookies = {
            "acf_auth": self.acf_auth,
        }
        datas = {
            'propId': propid,
            'propCount': propcount,
            'roomId': roomid,
            'bizExt': '{"yzxq":{}}',
        }
        html = r.post(url='https://www.douyu.com/japi/prop/donate/mainsite/v1', headers=self.header, cookies=cookies, data=datas)
        info_json = json.loads(html.text)
        gift_json = info_json.get('data').get('list')
        if gift_json:
            logger.info('给{0}赠送小礼物{1}成功'.format(roomid, propid))
        else:
            logger.info('给{0}赠送小礼物{1}失败'.format(roomid, propid))

    # 签到这里有个坑,签到后前端的签到按钮不会改变（实际上已经签到）
    def check_in(self, roomId):
        cookies = {
            "acf_auth": self.acf_auth,
            "acf_ccn": self.ctn,
        }
        datas = {
            'rid': roomId,
            'ctn': self.ctn
        }
        html = r.post(url="https://www.douyu.com/japi/roomuserlevel/apinc/checkIn", headers=self.header, cookies=cookies, data=datas)
        info_json = json.loads(html.text)
        if info_json.get('msg') == '请求成功':
            logger.info('{}签到成功'.format(roomId))
        else:
            logger.info('{}签到失败'.format(roomId))

    # 获取所有关注的房间(直播中)
    def get_live_room(self):
        fo = []
        cookies = {
            "acf_auth": self.acf_auth,
        }
        html = r.get(url="https://www.douyu.com/wgapi/livenc/liveweb/follow/headList?page=1", headers=self.header, cookies=cookies)
        info_json = json.loads(html.text)
        follows = info_json.get('data')
        if follows:
            follows = follows.get('list')
            for follow in follows:
                fo.append(dict(follow).get('room_id'))
            logger.info('获取关注的开播房间成功,房间号为' + str(fo))
        elif info_json.get('msg') == '用户未登陆或token已过期':
            logger.info('acf_auth令牌错误')
        else:
            logger.info('获取关注房间发生未知错误')
        return fo

    # 获取鱼塘信息
    def get_sharkinfo(self, roomId):
        cookies = {
            "acf_auth": self.acf_auth,
            "acf_ccn": self.ctn,
        }
        html = r.get(url="https://www.douyu.com/japi/activepointnc/api/sharkInfo?rid={}".format(roomId), headers=self.header, cookies=cookies)
        info_json = json.loads(html.text)
        data_json = info_json.get('data')
        if data_json:
            level = data_json.get('sharkLevel')
            point = data_json.get('userActivePoint')
            logger.info('鲨鱼等级: ' + level + '鱼粮: ' + point)
        else:
            logger.info('获取鱼塘信息失败')

    # 鱼塘寻宝
    def do_lottery(self, roomId):
        cookies = {
            "acf_auth": self.acf_auth,
            "acf_ccn": self.ctn,
        }
        datas = {
            'rid': roomId,
            'type': 0,
            'version': 1.2,
            "ctn": self.ctn,
        }
        html = r.post(url="https://www.douyu.com/japi/activepointnc/api/dolottery", headers=self.header, cookies=cookies, data=datas)
        info_json = json.loads(html.text)
        if info_json:
            if info_json.get('msg') == '操作成功':
                logger.info('寻宝成功')
            elif info_json.get('msg') == '今日次数不足':
                logger.info('今日次数不足')
            else:
                logger.info('未知错误')


    # 获取有粉丝牌的房间号
    def get_fans_rid(self):
        cookies = {
            "acf_auth": self.acf_auth,
        }

        html = r.get(url="https://www.douyu.com/member/cp/getFansBadgeList", headers=self.header, cookies=cookies)
        roomid = re.compile('(?<=<a href=\"/)\d+(?=[\s\S]*class="anchor--name)').findall(html.text)
        return roomid

    # 每日任务
    def daily_task(self, id):
        # 博览群书：在关注的3个开播房间（30级以上）签到。id=14
        cookies = {
            "acf_auth": self.acf_auth,
        }
        datas = {
            'id': id,
            'ctn': self.ctn,
        }
        html = r.post(url="https://www.douyu.com/japi/tasksys/ytxb/getPrize", headers=self.header, cookies=cookies, data=datas)
        info_json = json.loads(html.text)
        if info_json.get('msg') == '奖励已领取':
            logger.info('奖励已领取')
        elif info_json.get('msg') == '任务未完成，无法领取奖励':
            logger.info('任务未完成，无法领取奖励')
        else:
            logger.info('完成任务{}'.format(id))
>>>>>>> 20210328


# 获取鱼塘信息
def get_sharkinfo(roomId):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Referer": "https://www.douyu.com/",
    }
    cookies = {
        "acf_auth": ACF_AUTH,
        "acf_ccn": CTN,
    }
    html = r.get(url="https://www.douyu.com/japi/activepointnc/api/sharkInfo?rid={}".format(roomId), headers=header, cookies=cookies)
    info_json = json.loads(html.text)
    data_json = info_json.get('data')
    if data_json:
        level = data_json.get('sharkLevel')
        point = data_json.get('userActivePoint')
        print('鲨鱼等级: ', level)
        print('鱼粮: ', point)
    else:
        print('获取鱼塘信息失败')


# 鱼塘寻宝
def do_lottery(roomId):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Referer": "https://www.douyu.com/",
    }
    cookies = {
        "acf_auth": ACF_AUTH,
        "acf_ccn": CTN,
    }
    datas = {
        'rid': roomId,
        'type': 0,
        'version': 1.2,
        "ctn": CTN,
    }
    html = r.post(url="https://www.douyu.com/japi/activepointnc/api/dolottery", headers=header, cookies=cookies, data=datas)
    info_json = json.loads(html.text)
    if info_json:
        if info_json.get('msg') == '操作成功':
            print('寻宝成功')
        elif info_json.get('msg') == '今日次数不足':
            print('今日次数不足')
        else:
            print('未知错误')


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(set_task, 'cron', hour=16, minute=45, second=20)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    # douyu = Douyu()
    # douyu.get_live_room()
    # douyu.get_backpack()
    # send_gift(268, 1, 5190741)
<<<<<<< HEAD
    # check_in(5190741)
    # get_sharkinfo(52319)
    do_lottery(52319)
=======
    # douyu.check_in(3494554)
    # get_sharkinfo(52319)
    # douyu.do_lottery(52319)
    # print(douyu.get_fans_rid())
    # daily_task(14)
>>>>>>> 20210328
