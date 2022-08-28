import random
from time import time, localtime
import cityinfo
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os
import requests             #调用requests库import json
from lxml import etree


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token

def getNe():
    url = 'https://v0.tianqiapi.com/?version=today&unit=m&language=zh&query=%E7%BA%BD%E7%BA%A6&appid=43656176&appsecret=I42og6Lm'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400"}  # 构建请求头  模拟浏览器访问

    r = requests.get(url, headers=headers)
    data = {}
    data['phrase'] = r.json()['day']['phrase']
    data['narrative'] = r.json()['day']['narrative']
    data['city'] = r.json()['city']
    print(data)
    return data

def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday


    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_loveWords():
    url = 'https://api.lovelive.tools/api/SweetNothings/Web/1'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400"}  # 构建请求头  模拟浏览器访问

    r = requests.get(url, headers=headers)
    data = r.json()['returnObj']['content']
    return data

def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en

def tianxing():
    url1 = 'http://api.tianapi.com/healthtip/index?key=5b69ce0e74795efa5c285e6f0c34947d'
    url2 = 'http://api.tianapi.com/star/index?key=5b69ce0e74795efa5c285e6f0c34947d&astro=天蝎座'
    url3 = 'http://api.tianapi.com/caihongpi/index?key=5b69ce0e74795efa5c285e6f0c34947d'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400"}  # 构建请求头  模拟浏览器访问

    r = requests.get(url1, headers=headers)
    healthtip = r.json()["newslist"][0]["content"]
    r = requests.get(url2, headers=headers)
    star = r.json()["newslist"][8]["content"]
    r = requests.get(url3, headers=headers)
    caihongpi = r.json()["newslist"][0]["content"]
    return healthtip, star, caihongpi


def get_weather1():
    url1 = 'https://www.tianqiapi.com/life/lifepro?appid=64112834&appsecret=zDfVi1p5&cityid=101190801'
    url2 = 'https://www.yiketianqi.com/free/day?appid=64112834&appsecret=zDfVi1p5&cityid=101190801&unescape=1'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400"}  # 构建请求头  模拟浏览器访问

    r = requests.get(url1, headers=headers)
    LifesIndex = []
    chuanyi = r.json()["data"]["chuanyi"]
    fangshai = r.json()["data"]["fangshai"]
    guangjie = r.json()["data"]["guangjie"]
    pijiu = r.json()["data"]["pijiu"]
    huazhuang = r.json()["data"]["huazhuang"]
    xinqing = r.json()["data"]["xinqing"]
    yuehui = r.json()["data"]["yuehui"]
    yusan = r.json()["data"]["yusan"]
    LifesIndex.append(xinqing)
    LifesIndex.append(chuanyi)
    LifesIndex.append(fangshai)
    LifesIndex.append(guangjie)
    LifesIndex.append(huazhuang)
    LifesIndex.append(yuehui)
    LifesIndex.append(yusan)
    LifesIndex.append(pijiu)
    # print(LifesIndex)
    Weathers = []
    r2 = requests.get(url2, headers=headers)
    city = r2.json()["city"]
    date = r2.json()["date"] + ' ' + r2.json()["week"]
    wea = r2.json()["wea"]
    tem_day = r2.json()["tem_day"]
    tem_night = r2.json()["tem_night"]
    air = r2.json()["air"]
    pressure = r2.json()["pressure"]
    humidity = r2.json()["humidity"]
    Weathers.append(city)
    Weathers.append(date)
    Weathers.append(wea)
    Weathers.append(tem_day)
    Weathers.append(tem_night)
    Weathers.append(air)
    Weathers.append(pressure)
    Weathers.append(humidity)
    # print(Weathers)
    return Weathers, LifesIndex

def Scorpio():
    url = 'https://www.d1xz.net/yunshi/today/Scorpio/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400"}
    # 构建请求头  模拟浏览器访问
    response = requests.get(url, headers=headers)  # requests下载网页，用headers请求头
    content = response.content.decode('utf-8')  # 解码
    html = etree.HTML(content)  # etree解析网页

    dress = html.xpath('//*[@class="txt"]/p/text()')
    return dress[0]

def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, note_ch, note_en, loves, Scorpio,Weathers, LifesIndex,healthtip, star, caihongpi,datas):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": '今天是：' + "{} {}".format(today, week),
                "color": get_color()
            },
            "city": {
                "value": city_name + '今天：' + weather,
                "color": get_color()
            },
            "city1": {
                "value": datas['city'] + '今天：' + datas['phrase'],
                "color": get_color()
            },
            "tem": {
                "value": datas['narrative'],
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "weather1": {
                "value": "天气：" + weather,
                "color": get_color()
            },
            "min_temperature": {
                "value": '最低温度：' + min_temperature,
                "color": get_color()
            },
            "max_temperature": {
                "value": '最高温度：' + max_temperature,
                "color": get_color()
            },
            "love_day": {
                "value": '今天是我们在一起的' + love_days + '天！',
                "color": get_color()
            },
            "love": {
                "value": '今天是我们在一起的' + love_days + '天',
                "color": get_color()
            },
            "love2": {
                "value": '是我像你表白的第' + love_days + '天❤❤❤',
                "color": get_color()
            },
            "loves": {
                "value": '今天要对你说的话：' + '\n' + loves,
                "color": get_color()
            },
            "text": {
                "value": '下面是今日生活指数，要认真查看哦！😘(づ￣ 3￣)づ',
                "color": get_color()
            },
            "Scorpio": {
                "value": '今日运势：'+ '\n' + Scorpio,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {
                "value": '今天的鸡汤：' + '\n' + note_ch,
                "color": get_color()
            },
            "air": {
                "value": '空气指数：' + Weathers[5],
                "color": get_color()
            },
            "pressure": {
                "value": '气压：' + Weathers[6],
                "color": get_color()
            },
            "humidity": {
                "value": '湿度：' + Weathers[7],
                "color": get_color()
            },
            "xinqing": {
                "value": LifesIndex[0]['name'] + '：' + LifesIndex[0]['desc'],
                "color": get_color()
            },
            "chuanyi": {
                "value": LifesIndex[1]['name'] + '：' + LifesIndex[1]['desc'],
                "color": get_color()
            },
            "fangshai": {
                "value": LifesIndex[2]['name'] + '：' + LifesIndex[2]['desc'],
                "color": get_color()
            },
            "guangjie": {
                "value": LifesIndex[3]['name'] + '：' + LifesIndex[3]['desc'],
                "color": get_color()
            },
            "huazhuang": {
                "value": LifesIndex[4]['name'] + '：' + LifesIndex[4]['desc'],
                "color": get_color()
            },
            "yuehui": {
                "value": LifesIndex[5]['name'] + '：' + LifesIndex[5]['desc'],
                "color": get_color()
            },
            "yusan": {
                "value": LifesIndex[6]['name'] + '：' + LifesIndex[6]['desc'],
                "color": get_color()
            },
            "pijiu": {
                "value": LifesIndex[7]['name'] + '：' + LifesIndex[7]['desc'],
                "color": get_color()
            },
            "healthtip": {
                "value": "健康提示：" + healthtip,
                "color": get_color()
            },
            "star": {
                "value": "星座运势" + star,
                "color": get_color()
            },
            "caihongpi": {
                "value": caihongpi,
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if int(birth_day) == 0:
            birthday_data = "今天是{}的生日哦！祝{}生日快乐！{}今天要开开心心！".format(value["name"], value["name"], value["name"])
        elif int(birth_day) > 0 and int(birth_day) <= 10:
            birthday_data = "{}的生日只有{}天啦！".format(value["name"], birth_day)
        else:
            birthday_data = "距离{}的生日还有{}天！".format(value["name"], birth_day)
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入省份和市获取天气信息
    province, city = config["province"], config["city"]
    weather, max_temperature, min_temperature = get_weather(province, city)
    # 获取词霸每日金句
    note_ch, note_en = get_ciba()
    # 获取每日情话
    loves = get_loveWords()
    Scorpio = Scorpio()
    Weathers, LifesIndex = get_weather1()
    healthtip, star, caihongpi = tianxing()
    datas = getNe()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, city, weather, max_temperature, min_temperature, note_ch, note_en, loves, Scorpio,Weathers, LifesIndex,healthtip, star, caihongpi,datas)
    os.system("pause")
