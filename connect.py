#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import traceback,time,math

LOGFILE="connect.log"
LOGLEVEL=("DEBUG","INFO","WARNING","ERROR","FATAL")

def log(msg,l=1,end="\n",logfile=LOGFILE):
    st=traceback.extract_stack()[-2]
    lstr=LOGLEVEL[l]
    now_str="%s %03d"%(time.strftime("%y/%m/%d %H:%M:%S",time.localtime()),math.modf(time.time())[0]*1000)
    if l<3:
        tempstr="%s [%s,%s:%d] %s%s"%(now_str,lstr,st.name,st.lineno,str(msg),end)
    else:
        tempstr="%s [%s,%s:%d] %s:\n%s%s"%(now_str,lstr,st.name,st.lineno,str(msg),traceback.format_exc(limit=5),end)
    print(tempstr,end="")
    if l>=1:
        with open(logfile,"a") as f:
            f.write(tempstr)

import requests,sys,json

def net_login(username,password_hash):
    """
        request: http://net.tsinghua.edu.cn/do_login.php
        method: POST
        post data:
            action: login
            username: username
            password: {MD5_HEX}32_bit_hex
            ac_id: 1
    """
    url='https://net.tsinghua.edu.cn/do_login.php'
    headers={"Accept":"*/*","Host":"net.tsinghua.edu.cn"}
    data={'action':'login','username':username,'password':password_hash,'ac_id':'1'}
    log("posting: %s"%(url))
    try:
        post=requests.post(url,headers=headers,data=data,timeout=10)
        content=post.content.decode(post.encoding)
        log('%d: "%s"'%(post.status_code,content))
    except Exception as e:
        log("error happened: %s"%(e),l=2)

def test_network(test_url):
    try:
        headers={"Accept":"*/*"}
        log("getting: %s"%(test_url))
        get=requests.get(test_url,headers=headers,timeout=10)
        if get.status_code==200:
            return 0
        else:
            return str(get.status_code)
    except Exception as e:
        return str(e)

def test_and_reconnent(username,password_hash):
    """test online or not, if not, login"""
    import random
    url_pool=["http://baidu.com","http://bing.com","http://github.com"]
    test_re=test_network(random.choice(url_pool))
    if test_re==0:
        log("online already")
    else:
        log("not online(%s), reconnecting..."%(test_re))
        net_login(username,password_hash)

def gen_config():
    import getpass,hashlib
    username=input("username: ")
    password=getpass.getpass("password: ")
    password_hash='{MD5_HEX}'+hashlib.md5(password.encode('latin1')).hexdigest()
    with open("config.json","w") as f:
        config=json.dump({"username":username,"password_hash":password_hash},f)
    log("dumped username and password's hash to config.json")

if __name__ == '__main__':
    if len(sys.argv)>=2 and sys.argv[1]=="--test-first":
        with open("config.json","r") as f:
            config=json.load(f)
        username=config["username"]
        password_hash=config["password_hash"]
        test_and_reconnent(username,password_hash)
    elif len(sys.argv)>=2 and sys.argv[1]=="--connect":
        with open("config.json","r") as f:
            config=json.load(f)
        username=config["username"]
        password_hash=config["password_hash"]
        net_login(username,password_hash)
    elif len(sys.argv)>=2 and sys.argv[1]=="--gen-config":
        gen_config()
    else:
        log("Tsinghua Tunet auto-connect script\n--test-first\n--connect\n--gen-config")
