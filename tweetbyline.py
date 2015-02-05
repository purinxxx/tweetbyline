#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from line import LineClient, LineGroup, LineContact
from requests_oauthlib import OAuth1Session

mail = ''
password = ''

CK = '' # Consumer Key
CS = '' # Consumer Secret
AT = '' # Access Token
AS = '' # Accesss Token Secert

url = "https://api.twitter.com/1.1/statuses/update.json"

def tweet(text):
    params = {"status": text}
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(url, params = params)
    if req.status_code == 200:
        print "OK"
    else:
        print "Error: %d" % req.status_code


try:
    client = LineClient(mail, password) #メアド, パス
    #authToken = client.authToken
    #print authToken
    #client = LineClient(authToken="トークン")
    print "Logined"
except:
    print "Login Failed"

cnt = 0
for i in client.contacts:
    if str(i)[13:-1] == "twitter":  #ユーザー名「twitter」を探す（サブ垢）
        print cnt,str(i)[13:-1]
        break
    cnt+=1

friend = client.contacts[cnt]
while True:
    time.sleep(1)
    raw = friend.getRecentMessages(count=1)[0]
    if raw.contentType == 0:    #画像やスタンプは無視してテキストだけ処理する
        tmp = str(raw)[81:-2]   #なぜかインスタンス変数にアクセスできないので文字列化してスライス
        if tmp != "ok":
            print tmp
            if tmp == "stop":
                friend.sendMessage("ok")
                sys.exit()
            else:
                tweet(tmp)
                friend.sendMessage("ok")

