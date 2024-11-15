import json
import re
import time

import requests
from lxml import etree
import logging
from config_info import bot, userId, proxy


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',

    'cookie':'_ym_uid=1710753523251935900; captcha_v4_user=332855da0f874221bd2bf911818681c1; ak_bmsc=660F44590E276CB0E202922BC5952C24~000000000000000000000000000000~YAAQP2YzuAagNSWTAQAA/ivAJRm1t2wqTQcZh3bQP/NU7Z/zofCJzF6ZAnyI5qM3vT42cbzjl5y2qhw/A3950iS8Xo48KA5GdbznMvMT5oVxeFexJ5R49SaGONaEu8o3FJeCtdAF8t2T8g2wnuCFtY5plWPUxUCwx/hfqFBBIIQiU26HG1252oWopAW/Cfx5dgu5oVGo/i/8WZ/3IL0fTsBLxmplUgb/9dQDSDQjcWAD6E40xajepP2ylmZezXlUUI6LGsMS/Bu8zv845QfdeRrveLJjA4mU9ji7spG8g/wJ+Y2Jxlqr+sW6sRqNnhzlpX+od3cAobVmkXBApjrLvZnK9j/ueQuFwbZljukYOThk3L0BDBApgpnMtVYu/uAIu4GYyfYWzOV/jQ==; _ga=GA1.1.1973894851.1731505174; bitget_lang=zh-CN; BITGET_LOCAL_COOKIE={%22bitget_lang%22:%22zh-CN%22%2C%22bitget_unit%22:%22USD%22%2C%22bitget_showasset%22:true%2C%22bitget_theme%22:%22white%22%2C%22bitget_layout%22:%22right%22%2C%22bitget_valuationunit%22:1%2C%22bitget_valuationunitandfiat%22:1%2C%22bitgt_login%22:false}; theme=white; _ga_clientid=1973894851.1731505174; _ga_sessionid=1731505174; _dx_kvani5r=e06bb641e802d601e4861c7a018f2152f25c659f5e7d80d6aa2f6fcc030eeec41a63f70d; bt_rtoken=; bt_sessonid=; bt_newsessionid=; dy_token=6734ac198Qz38afWcmeaIBAO9ZWzDTmUUml2tAm1; _ym_d=1731505178; _ym_isad=1; afUserId=54004282-86bf-4180-83d4-e17c6e4a4785-p; AF_SYNC=1731505178954; _ym_visorc=b; OptanonAlertBoxClosed=Wed%20Nov%2013%202024%2021:39:43%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); OptanonConsent=isMarketing=1&isStatistic=1; __cf_bm=PJm1c3IFTS3Ora5xHWDwl764owY6kq5.KPkfpyBgtF4-1731505185-1.0.1.1-H3k43WDAdPVVlbCncb918ee5OruawDKmFizw2ZRv.BtDohw5y5ycdXgalYHdVrFA3RqFAnZoAenfLYaL429yTA; _cfuvid=jn531YhWCba.4cj11ZMnmdCJjh.IFgRum_Vzxq6dldE-1731505185961-0.0.1.1-604800000; bm_sv=7C038692AD937BA192BCF677DB58D43C~YAAQP2YzuA2vNSWTAQAASp3CJRkVgitonTFhrr8LRxZgV19nzrXq5SmmVJuZ7dUO5PGMoFr1lDOqQ7Gi1Y+cDxyB6Mitd+AQHutHnOpHToaxV8+aKM0a09PMSCxTxGFEQ5rJ3UE5tTZlUKPXN6XEChVyU1dUxwa0INU/zEwWedE21bbblDrc1PYDeIc+Dh9liFXHkXtVmDszsm2KYIxp6E4V7kpgQFDmqTzrjws8HQEE218Cabgcqo/+eO0J/YFcpw==~1; _ga_Z8Q93KHR0F=GS1.1.1731505174.1.1.1731505333.21.0.0',

    'if-none-match':'d1686cf3717d6e7c95f05ffebaa24189db1398898cbf69afa42ded3519a4aef7',
    'sec-ch-ua':'"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'

}


logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)s: %(message)s')

def symbolinfo():

    logging.info("开始进行bitget数据爬取")
    url = 'https://www.bitget.com/support/sections/12508313443483' #请求地址

    count_true = 0 #计数器，计算成功次数
    count_false = 0  # 计数器，计算错误次数
    ids = []
    while True:

        res = ''
        try:
            res = requests.get(url, headers=header, proxies=proxy).text

            if count_true%1000 == 0:
                logging.info(f'bitget存活测试，程序正在运行，当前运行次数为{count_true}')
            count_true += 1
        except:
            logging.info(f"bitget_xinbi第{count_false}运行错误")

        try:

            tree = etree.HTML(res)

            content = tree.xpath('//script[@id="__NEXT_DATA__"]/text()')[0]  # xpath解析

            # 解析JSON数据
            listing = json.loads(content)


            latest_listing = listing['props']['pageProps']['sectionArticle']['items'][0]

            id = latest_listing['contentId']
            title = latest_listing['title']
            releaseDate = int(latest_listing['showTime']) # 发布时间


            content_url = f'https://www.bitget.com/zh-CN/support/sections/{id}'

            if id not in ids:
                bot.send_message(userId, title)
                bot.send_message(userId, content_url)

                current_time = int(round(time.time() * 1000))  # 当前时间

                differ = (current_time - releaseDate) // 1000  # 相差的时间戳
                differ_hours = differ // 3600  # 相差的小时
                differ_mintus = (differ % 3600) // 60  # 相差的分
                differ_sec = differ % 60  # 相差的秒
                message = f'与发布时间相差{differ_hours}时{differ_mintus}分{differ_sec}秒'
                bot.send_message(userId, message)
                ids.append(id)
                logging.info(message)

        except Exception as e:
            logging.info(e)
            logging.info("网页解析失败，可能是由于爬取次数太多")

        time.sleep(5)  # 每隔5秒爬取一次

symbolinfo()