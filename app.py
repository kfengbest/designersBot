#coding=utf8

from wxpy import *

import io, os, json, time
import re
import requests
import urllib

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

def FindUrl(string): 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url 

api_key_str = ''
cms_endpoint = ''
with open('config_secret.json') as config:
    dataJson = json.load(config)
    api_key_str = dataJson["tuling_api_key"]
    cms_endpoint = dataJson["cms_endpoint"]

tuling = Tuling(api_key=api_key_str)

abs_path = os.path.abspath('.')
file_save_path = abs_path
dir_name = 'saved_files'
wxpy_file_path = os.path.join(file_save_path,dir_name)
if dir_name not in os.listdir(file_save_path):
    os.mkdir(wxpy_file_path)

bot = Bot(cache_path=os.path.join(wxpy_file_path, 'wxpy_cache.pkl'))
bot.enable_puid(path=os.path.join(wxpy_file_path, 'wxpy_puid.pkl'))

@bot.register(Group)
def auto_reply(msg):

    if msg.type == TEXT:
        
        urls = FindUrl(msg.text)
        for url in urls:
            strName = {'author':msg.member.name}
            userName =  urllib.urlencode(strName)
            extUrl = "{0}?op=CollectUrlViaRobot&url={1}&{2}".format(cms_endpoint, url,userName)
            rExtUrl = requests.get(extUrl)
            resJson = rExtUrl.json()
            print(extUrl)
            if resJson['result_code'] == 0:
                resMsg = u"@{0} 真棒，又一条新资源被录了".format(msg.member.name)
                msg.reply_msg(resMsg)
            elif resJson['result_code'] == 2:
                resMsg = u"@{0} 这条被收录多次了，看来很火".format(msg.member.name)
                msg.reply_msg(resMsg)

        if isinstance(msg.chat, Group) and not msg.is_at:
            return
        else:
            tuling.do_reply(msg)

# 堵塞线程
embed()