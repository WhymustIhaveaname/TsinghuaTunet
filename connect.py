#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import traceback,time,math

LOGFILE="connect.log"
ERRORFILE="error.log"
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
        if l>=2:
            with open(ERRORFILE,'a') as f:
                f.write(tempstr)

# used in auth4 login
# I cannot understand this
# but I have to include it
import struct
int2byte = struct.Struct(">B").pack
def xEncode(str, key):
        def s(a, b):
            c = len(a)
            v = []
            for i in range(0, c, 4):
                v.append(
                    ord(a[i]) |
                    lshift(0 if i + 1 >= len(a) else ord(a[i + 1]), 8) |
                    lshift(0 if i + 2 >= len(a) else ord(a[i + 2]), 16) |
                    lshift(0 if i + 3 >= len(a) else ord(a[i + 3]), 24)
                )
            if b:
                v.append(c)
            return v

        def l(a, b):
            d = len(a)
            c = lshift(d - 1, 2)
            if b:
                m = a[d - 1]
                if m < c - 3 or m > c:
                    return None
                c = m
            for i in range(d):
                a[i] = int2byte(a[i] & 0xff) \
                    + int2byte(rshift(a[i], 8) & 0xff) \
                    + int2byte(rshift(a[i], 16) & 0xff) \
                    + int2byte(rshift(a[i], 24) & 0xff)
            if b:
                return b''.join(a)[:c]
            else:
                return b''.join(a)

        def rshift(x, n):
            return x >> n

        def lshift(x, n):
            return (x << n) & ((1 << 32) - 1)

        if str == '':
            return ''
        v = s(str, True)
        k = s(key, False)
        while len(k) < 4:
            k.append(None)
        n = len(v) - 1
        z = v[n]
        c = 0x86014019 | 0x183639A0
        q = 6 + 52 // (n + 1)
        d = 0
        while 0 < q:
            q -= 1
            d = d + c & (0x8CE0D9BF | 0x731F2640)
            e = rshift(d, 2) & 3
            for p in range(n):
                y = v[p + 1]
                m = rshift(z, 5) ^ lshift(y, 2)
                m += rshift(y, 3) ^ lshift(z, 4) ^ (d ^ y)
                m += k[(p & 3) ^ e] ^ z
                z = v[p] = v[p] + m & (0xEFB8D130 | 0x10472ECF)
            p = n
            y = v[0]
            m = rshift(z, 5) ^ lshift(y, 2)
            m += rshift(y, 3) ^ lshift(z, 4) ^ (d ^ y)
            m += k[(p & 3) ^ e] ^ z
            z = v[n] = v[n] + m & (0xBB390742 | 0x44C6F8BD)
        return l(v, False)

import requests,sys,json,hashlib,base64,hmac,urllib3

TIMEOUT=3

# again auth4's weird stuffs
def weird_base64_encode(s):
    a='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    b='LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA'
    s=base64.b64encode(s).decode()
    return s.translate({ord(x): y for (x, y) in zip(a, b)}).encode()

def auth4_login(username,password):
    if password==None:
        log("please update (re-generate) config to get support for auth4",l=2)
        return -4
    headers={"Accept":"*/*","Host":"auth4.tsinghua.edu.cn",
             "User-Agent":"Mozilla/5.0","Accept-Encoding":"gzip, deflate","Accept-Language":"zh;q=0.9,en;q=0.8"}
    # get challenge. I do not know why
    try:
        url="https://auth4.tsinghua.edu.cn/cgi-bin/get_challenge"
        params={'callback':'callback','username':username,'ip':'','double_stack':'1','_':int(time.time()*1000)}
        g1=requests.get(url,headers=headers,params=params,timeout=TIMEOUT)
        c1=g1.content.decode(g1.encoding).strip()
        challenge=json.loads(c1[len("callback("):-1])
        token=challenge['challenge']
        hmd5=hmac.new(token.encode(),msg=None,digestmod='md5').hexdigest()
        ip=challenge['online_ip']
        del url,params,g1
    except:
        log("get challenge failed",l=3)
        return -1
    #
    try:
        url="http://usereg.tsinghua.edu.cn/ip_login_import.php"
        params={'actionType': 'searchNasId', 'ip': ip}
        g2=requests.post(url,headers=headers,data=params,timeout=TIMEOUT)
        c2=g2.content.decode(g2.encoding).strip()
        if c2=='fail':
            ac_id=1
        elif c2.isnumeric():
            ac_id=int(c2)
            log("get ac_id: %s"%(ac_id))
        else:
            log("get ac_id abnormal: %s"%(c2),l=2)
            ac_id=1
        del url,params,g2
    except:
        log("exception in getting ac_id",l=3)
        return -2
    # login!
    n=200;typ=1
    try:
        url="https://auth4.tsinghua.edu.cn/cgi-bin/srun_portal"
        info='{SRBX1}'+weird_base64_encode(xEncode(json.dumps({'username':username,'password':password,'ip':ip,'acid':ac_id,'enc_ver':'srun_bx1',}),token)).decode()
        chksum=hashlib.sha1((token+username+token+hmd5+token+'%d'%(ac_id)+token+ip+token+'%d'%(n)+token+'%d'%(typ)+token+info).encode()).hexdigest()
        params={'callback':'callback','action':'login','username':username,'password':'{MD5}'+hmd5,
                'ac_id':ac_id,'ip':ip,'double_stack':'1','info':info,'chksum':chksum,'n':n,'type':typ,'_':int(time.time()*1000)}
        g3=requests.get(url,headers=headers,params=params,timeout=TIMEOUT)
        c3=g3.content.decode(g3.encoding).strip()
        c3=json.loads(c3[len("callback("):-1])
        if c3['error']=='ok':
            log({k:c3[k] for k in ["client_ip","error","res","suc_msg"] if k in c3},l=2)
        else:
            log(c3,l=2)
        del url,params,g3
    except:
        log("exception in auth4 login",l=3)
        return -3
    """
    try:
        from bs4 import BeautifulSoup #make output pretty
        url="https://auth4.tsinghua.edu.cn/succeed_wired.php"
        params={'ac_id':'1','username':'syr20','ip':ip}
        g4=requests.get(url,headers=headers,params=params,timeout=TIMEOUT)
        c4=g4.content.decode('utf-8').strip() # g4.encoding is ISO-8859-1 but actually it is utf8
        soup = BeautifulSoup(c4,'lxml')
        log('\t'.join([i for i in soup.text.split('\n') if i!='']))
    except:
        log("",l=3)
        return -5"""

"""def usereg_login(username,password_hash):
    #login via usereg.tsinghua.edu.cn's '准入代认证'
    log("usereg's login is auth4.",end=" press enter to quit...");input()
    s=requests.Session()
    s.headers={"Accept":"*/*","Host":"usereg.tsinghua.edu.cn","User-Agent":"Mozilla/5.0","Accept-Encoding":"gzip, deflate"}
    data={'action':'login','user_login_name':username,'user_password':password_hash.replace("{MD5_HEX}","")}
    p1=s.post("http://usereg.tsinghua.edu.cn/do.php",data=data)
    c1=p1.content.decode(p1.encoding)
    s.headers['Cookie']=p1.headers['Set-Cookie'].split(';')[0]"""

def net_login(username,password_hash,password):
    """
        request: http://net.tsinghua.edu.cn/do_login.php
        method: POST
        post data:
            action: login
            username: username
            password: {MD5_HEX}32_bit_hex
            ac_id: 1
    """
    url='http://net.tsinghua.edu.cn/do_login.php'
    headers={"Accept":"*/*","Host":"net.tsinghua.edu.cn",
             "User-Agent":"Mozilla/5.0","Accept-Encoding":"gzip, deflate","Accept-Language":"zh;q=0.9,en;q=0.8"}
    data={'action':'login','username':username,'password':password_hash,'ac_id':'1'}
    log("posting: %s"%(url))
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        post=requests.post(url,headers=headers,data=data,timeout=TIMEOUT,verify=False,allow_redirects=True)
        content=post.content.decode("gbk") # post.encoding is "ISO-8859-1" but it is wrong
    except Exception as e:
        log("error happened: %s"%(e),l=3)

    if "auth4.tsinghua.edu.cn" in content:                    #see comments for test_network
        log("Tsinghua wants you to login via auth4, trying auth4...",l=2)
        auth4_login(username,password)
    else:
        log('%d: "%s"'%(post.status_code,content),l=2)

def test_network(test_url):
    """
        test by getting test_url
        some times tsinghua wants you to login via auth4
        so if there is 'auth4.tsinghua.edu.cn' in return webpage then return 1
        meaning 'trying to login via auth4'
    """
    try:
        headers={"Accept":"*/*"}
        log("getting: %s"%(test_url))
        get=requests.get(test_url,headers=headers,timeout=10)
        if get.status_code==200:
            content=get.content.decode(get.encoding)
            if "auth4.tsinghua.edu.cn" in content:
                return 1                                       #some times tsinghua wants you to login via auth4
            else:
                return 0
        else:
            return "get.status_code=%d"%(get.status_code,)
    except Exception as e:
        return str(e)

def test_and_reconnent(username,password_hash,password):
    """test online or not, if not, login"""
    import random
    url_pool=["https://baidu.com","https://bing.com","https://github.com","http://baidu.com","http://bing.com","http://github.com"]
    #url_pool=["http://net.tsinghua.edu.cn",] # for debugging
    test_re=test_network(random.choice(url_pool))
    if test_re==0:
        log("online already")
    elif test_re==1:
        log("not online, reconnecting...\nreason: Tsinghua wants you to login via auth4",l=2)
        auth4_login(username,password)
    else:
        log("not online, reconnecting...\nreason: %s"%(test_re),l=2)
        net_login(username,password_hash,password)

def gen_config():
    import getpass,hashlib
    username=input("username: ")
    password=getpass.getpass("password: ")
    password_hash='{MD5_HEX}'+hashlib.md5(password.encode('latin1')).hexdigest()
    with open("config.json","w") as f:
        config=json.dump({"username":username,"password_hash":password_hash,'password':password,'version':'1.0.2'},f)
    log("dumped username and password's hash to config.json")

if __name__ == '__main__':
    help_msg="Tsinghua Tunet auto-connect script\n--test-first\n--connect\nconnect-auth4\n--gen-config"
    if len(sys.argv)>=2 and sys.argv[1] in ("--test-first","--connect","--connect-auth4","--connect-usereg"):
        try:
            with open("config.json","r") as f:
                config=json.load(f)
            username=config["username"]
            password_hash=config["password_hash"]
            if 'password' in config:
                password=config['password']
            else:
                log("please update (re-generate) config to get support for auth4",l=2)
                password=None
        except:
            log("load config.json failed. make sure a config file is generated by --gen-config")
        else:
            if sys.argv[1]=="--test-first":
                test_and_reconnent(username,password_hash,password)
            elif sys.argv[1]=="--connect":
                net_login(username,password_hash,password)
            elif sys.argv[1]=="--connect-auth4":
                auth4_login(username,password)
            elif sys.argv[1]=="--connect-usereg":
                usereg_login(username,password_hash)
            else:
                log(help_msg)
    elif len(sys.argv)>=2 and sys.argv[1]=="--gen-config":
        gen_config()
    else:
        log(help_msg)
