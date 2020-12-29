from google_trans_new import google_translator

import http.client
import hashlib
import urllib
import random
import json
import time

def parse_chinese(subtitle,site):
    """进行字幕翻译

        将输入的英文字幕转为中文，仅操作english_list部分
        参数
        ----------
        subtitle: list
            字幕的英文版
        site： “baidu”/"google"
            调用API的源
        返回值
        -------
        list
            中文字幕chinese_list

        """
    if site=='baidu':
        subtitleChinese=parse_chinese_baidu(subtitle)
        #print('baidu')
    if site=="google":
        subtitleChinese=parse_chinese_google(subtitle)
        #print("google")
    return subtitleChinese
def parse_chinese_baidu(subtitle):
    """进行字幕翻译(baidu版-API调用1次每秒——针对于字幕语句数)

    将输入的英文字幕转为中文，仅操作english_list部分
    参数
    ----------
    subtitle: list
        字幕的英文版

    返回值
    -------
    list
        中文字幕chinese_list

    """

    appid = '20201228000658138'  # 填写你的appid
    secretKey = 'hIjWX8gZBr83MnCgqZHL'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'en'  # 原文语种
    toLang = 'zh'  # 译文语种
    subtitleChinese = []
    for sub in subtitle:
        time.sleep(1)
        '''由于接口调用速率原因只能1次每秒'''
        salt = random.randint(32768, 65536)
        q = sub
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
            salt) + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)

            #result = json.load(result["trans_result"])
            #print(result)
            #print(result['trans_result'][0]['dst'])
            subtitleChinese.append(result['trans_result'][0]['dst'])

        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
    return subtitleChinese

def parse_chinese_google(subtitle):
    """进行字幕翻译(google版-无需翻墙功能)

    将输入的英文字幕转为中文，仅操作english_list部分

       参数
       ----------
       subtitle: list
           字幕的英文版

       返回值
       -------
       list
           中文字幕chinese_list
    """
    translator = google_translator()
    subtitleChinese = []
    for sub in subtitle:
        text = translator.translate(sub,lang_tgt='zh')
        subtitleChinese.append(text)
    return subtitleChinese

# if __name__ == '__main__':
#     test = []
#     test.append("Hello!")
#     test.append("What's your name?")
#     subtitleChinese = parse_chinese(test,site='baidu')
#     print(subtitleChinese)

