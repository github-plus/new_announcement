import json
import re
import time

import requests
from lxml import etree
import logging
from config_info import bot, userId, proxy


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',
    'cookie':'theme=dark; bnc-uuid=22489a2f-00e0-4070-8a5d-48b0c660604b; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221931a7ed175c79-063d3e4bfe08918-4c657b58-2073600-1931a7ed17613b4%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzMWE3ZWQxNzVjNzktMDYzZDNlNGJmZTA4OTE4LTRjNjU3YjU4LTIwNzM2MDAtMTkzMWE3ZWQxNzYxM2I0In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; BNC_FV_KEY=33d25250c053a38fb306bb4df0697a3bfeea2284; BNC_FV_KEY_T=101-wcSpJ7fbVdMrOGxrqa74pNbgKsecbCO0hmTei%2B%2Bnwxcin6NiF61cbbM5FpWayrs0rETv0AuZhdtYtaGJ68g0xg%3D%3D-agOaVui9xKzg3NP9XyQm6Q%3D%3D-c4; BNC_FV_KEY_EXPIRE=1731337939255; _ga=GA1.2.1726223954.1731318285; _gid=GA1.2.1300522883.1731318285; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+11+2024+17%3A44%3A53+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202410.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8eb656a2-de44-4ee6-8017-5815b8eb70f6&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A0%2CC0004%3A0%2CC0002%3A0&AwaitingReconsent=false',
    'if-none-match':'d1686cf3717d6e7c95f05ffebaa24189db1398898cbf69afa42ded3519a4aef7',
    'sec-ch-ua':'"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'

}


logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)s: %(message)s')

def symbolinfo():

    logging.info("开始进行数据爬取")
    url = 'https://www.binance.com/en/support/announcement/c-48?navId=48#/48' #请求地址

    count_true = 0 #计数器，计算成功次数
    count_false = 0  # 计数器，计算错误次数
    ids = []
    while True:

        res = ''
        try:
            res = requests.get(url, headers=header, proxies=proxy).text

            if count_true%1000 == 0:
                logging.info(f'存活测试，程序正在运行，当前运行次数为{count_true}')
            count_true += 1
        except:
            logging.info(f"bian_xinbi第{count_false}运行错误")

        try:

            tree = etree.HTML(res)


            content = tree.xpath('//script[@id="__APP_DATA"]/text()')[0] #xpath解析

            # 解析JSON数据
            listing = json.loads(content)
            listing_1 = listing['appState']['loader']['dataByRouteId']['d9b2']['catalogs'][0]   #第一页listing

            latest_listing = listing_1['articles'][0]

            id = latest_listing['id']
            title = latest_listing['title']
            releaseDate = latest_listing['releaseDate']  #发布时间
            code = latest_listing['code']
            content_url = f'https://www.binance.com/en/support/announcement/binance-will-add-act-i-the-ai-prophecy-act-and-peanut-the-squirrel-pnut-on-earn-buy-crypto-convert-margin-futures-{code}'
            if id not in ids:
                bot.send_message(userId, title)
                bot.send_message(userId, content_url)

                current_time = int(round(time.time() * 1000))  #当前时间
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

        time.sleep(5) #每隔5秒爬取一次

symbolinfo()