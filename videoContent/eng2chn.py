from google_trans_new import google_translator

import http.client
import hashlib
import urllib
import random
import json
import time
from tqdm import tqdm


class Translation(object):
    def __init__(self, english_list, site="baidu"):
        self.subtitle = english_list
        self.allTextChinese = ""
        self.videoTextChinese = []
        self.site = site

    def parse_chinese(self):
        """进行字幕翻译

            将输入的英文字幕转为中文，仅操作english_list部分
            参数
            ----------
            self.subtitle: list
                字幕的英文版
            self.site： “baidu”/"google"
                调用API的源
            返回值
            -------
            list
                中文字幕chinese_list

            """
        if self.site=='baidu':
            subtitleChinese=self.__parse_chinese_baidu(self.subtitle)
            #print('baidu')
        if self.site=="google":
            subtitleChinese=self.__parse_chinese_google(self.subtitle)
            #print("google")
        
        self.videoTextChinese = subtitleChinese
        self.allTextChinese = " ".join(self.videoTextChinese)
        return self.videoTextChinese, self.allTextChinese

    def __parse_chinese_baidu(self, subtitle):
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
        for sub in tqdm(subtitle):
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
                subtitleChinese.append("None")
            finally:
                if httpClient:
                    httpClient.close()
        return subtitleChinese

    def __parse_chinese_google(self, subtitle):
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
        for sub in tqdm(subtitle):
            text = translator.translate(sub,lang_tgt='zh')
            subtitleChinese.append(text)
        return subtitleChinese


if __name__ == '__main__':
    test = ["Hello!", "I am not fine", "Thank you"]
    T = Translation(test, site="baidu")
    subtitleChinese, allTextChinese = T.parse_chinese()
    print(subtitleChinese)
    print(allTextChinese)

