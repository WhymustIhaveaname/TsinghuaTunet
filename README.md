# Tsinghua Tunet auto-connect script.
## 清华校园网自动连接脚本.

### 使用方法

* `./connect.py --gen-config`: 生成配置文件;
* `./connect.py --connect`   : 使用 net.tsinghua.edu.cn 连接(推荐);
* `./connect.py --connect-auth4`: 使用 auth4.tsinghua.edu.cn 连接;
* `./connect.py --test-first`: 先测试网络, 不通再连接.

首先用 `./connect.py --gen-config` 按提示输入用户名密码生成配置文件, 之后用 `./connect.py --connect` 或 `./connect.py --test-first` 连接.

### 亮点

* 更短, 所以更少的八阿哥.
* 可以先测试网络是否通畅失败才重连.
* 有时清华会强制让人用 auth4.tsinghua.edu.cn 连接, 脚本能够自动跳转.
* 保存密码的哈希而不是明文(但是使用auth4需要提供密码明文).

### Pain in the neck

* 在 net 上下线后再用 auth4 登陆有时会失败.
* 有时下线时间长了之后连网关都 ping 不通, 就更不要说登陆了.
* 有时 auth 会报'请重新拿ip错误', 不知所云.

### 吐槽

* 清华的auth4/auth6系统是外包的, net是自己写的, 两个系统并行但是不不悖. 我怀疑 Pain in the neck 中的一些问题就是两个系统并存导致的.
* 外包的公司是一家叫"深澜"(srun)的公司,这个公司还负责包括北京理工大学在内的其他学校的网络管理软件. 网上对其软件的主要吐槽有:
    * 管杀不管埋: 没有 Linux 登陆客户端, 或者说有一个老版的但是不支持新协议;
    * url 参数中有大量不知所云又没用的部分 (这从代码的 auth4_login 函数的复杂程度可以看出来);
    * 协议中包含大量非标准实现, 使得很难写第三方登陆脚本 (比如代码的 xEncode 函数，根本不知道在做什么).

### 感谢

* [yuantailing/tunet-python](https://github.com/yuantailing/tunet-python) (我 fork 到了 [WhymustIhaveaname/tunet-python](https://github.com/WhymustIhaveaname/tunet-python))
* [深澜校园网登录的分析与python实现-北京理工大学版](https://blog.csdn.net/qq_41797946/article/details/89417722)
* [深澜认证协议分析,python模拟登录](https://zhuanlan.zhihu.com/p/122556315)


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

### Using crontab to execute at regular intervals

Crontab is a time-based job scheduler in Unix-like computer operating systems. Using `crontab -e` to edit its configuration file, then input
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
and save to run this script repeatedly every minute. Note that you should first cd to the directory of TsinghuaTunet, or it will leave a log file in crontab's default directory. Use `crontab -l` to confirm the configuration file is saved.
