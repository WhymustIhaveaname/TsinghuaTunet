# 清华校园网自动连接脚本
# Tsinghua Tunet auto-connect script

### 使用方法

* `./connect.py --gen-config`: 生成配置文件;
* `./connect.py --connect`   : 使用 net.tsinghua.edu.cn 连接 (推荐);
* `./connect.py --connect-auth4`: 使用 auth4.tsinghua.edu.cn 连接 (仅用于 debug);
* `./connect.py --connect-auth6`: 使用 auth6.tsinghua.edu.cn 连接 (测试中);
* `./connect.py --test-first`: 先测试网络, 不通再连接.

首先用 `./connect.py --gen-config` 按提示输入用户名密码生成配置文件, 之后用 `./connect.py --connect` 或 `./connect.py --test-first` 连接.

### 亮点

* 更短, 所以更少的八阿哥.
* 可以先测试网络是否通畅, 失败才重连.
* 有时清华会强制让人跳转 auth4.tsinghua.edu.cn 连接, 脚本能够自动跳转.
* 保存密码的哈希而不是明文 (但是使用auth4需要提供密码明文).
* 支持 ipv4 和 ipv6.

### Pain in the neck

* net 下线之后用 auth4 登陆会显示已经在线.
* 有时下线时间长了之后连网关都 ping 不通 (不知道为什么), 就更不要说登陆了.
* 登陆协议中的 ac_id 参数按“正统”的获取方法经常失败，只能通过 net 的返回获得. 如果设置了错误的 ac_id 会返回 `'ecode': '', 'error': 'login_error', 'error_msg': 'no_response_data_error', 'res': 'login_error'`, 如果按照 srun js 的逻辑直接设置 ac_id=1 则返回`'ecode': 'E2833', 'error': 'login_error', 'error_msg': 'E2833: Your IP address is not in the dhcp table. Maybe you need to renew the IP address.', 'res': 'login_error'`

### 吐槽

* 清华的 auth4/auth6 系统是外包的, net 是自己写的, 两个系统并行但是不不悖. 我怀疑 Pain in the neck 中的一些问题就是两个系统并存导致的.
* 外包的公司是一家叫"深澜"(srun)的公司,这个公司还负责包括北京理工大学在内的其他学校的网络管理软件. 网上对其软件的主要吐槽有:
    * 管杀不管埋: 没有 Linux 登陆客户端, 或者说有一个老版的但是不支持新协议;
    * url 参数中有很多没用的部分 (这从代码的 auth4_login 函数的复杂程度可以看出来);
    * 协议中包含数处非标准实现, 使得写第三方登陆脚本很难 (比如代码的 xEncode 函数，根本不知道在做什么).
* 深澜做这么多非标准操作和自定义 hash 的原因可能是让客户难以更换到其他公司替代之, 的确清华后来试图自己实现net也没能完全替代.
* 我本以为 usereg 中的准入代认证能够提供新的登陆方式, 结果也是深澜的 auth4/6.

### 感谢

* [yuantailing/tunet-python](https://github.com/yuantailing/tunet-python) (我 fork 到了 [WhymustIhaveaname/tunet-python](https://github.com/WhymustIhaveaname/tunet-python))
* [深澜校园网登录的分析与python实现-北京理工大学版](https://blog.csdn.net/qq_41797946/article/details/89417722)
* [深澜认证协议分析,python模拟登录](https://zhuanlan.zhihu.com/p/122556315)
* [ZenithalHourlyRate/thuservices/utils.md#校园网认证工具汇总](https://github.com/ZenithalHourlyRate/thuservices/blob/master/utils.md#%E6%A0%A1%E5%9B%AD%E7%BD%91%E8%AE%A4%E8%AF%81%E5%B7%A5%E5%85%B7%E6%B1%87%E6%80%BB)

### Hosts

In case any one needs related IPs.
```
166.111.204.120                net.tsinghua.edu.cn
101.6.4.100                    auth4.tsinghua.edu.cn
2402:f000:1:414:101:6:4:100    auth6.tsinghua.edu.cn
```

### 使用crontab重复执行脚本

Crontab是Linux系统中基于时间的任务管理程序。使用`crontab -e`以编辑其配置文件，输入
```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# * * * * * <command to execute>
* * * * * cd /dir/to/TsinghuaTunet && ./connect.py --test-first
```
并且保存退出来让脚本每分钟重复执行。注意要先cd至TsinghuaTunet的文件夹下，否则它的日志文件会留在当前文件夹。使用`crontab -l`确认配置被保存了。

### Usage

* `./connect.py --gen-config`: Generate a configure file including your username and password's hash.
* `./connect.py --connect`   : Connect directly.
* `./connect.py --test-first`: First test network by getting webpage of one of Bing, GitHub and Baidu, connect if failed.

First, use `./connect.py --gen-config` to generate a configure file. Then try `./connect.py --connect` or `./connect.py --test-first`.

### Feature

* Short so fewer bugs.
* Able to test network and reconnect if the test fails.
* Save password's hash rather than plaintext.
