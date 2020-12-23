# Tsinghua Tunet auto-connect script.
## 清华校园网自动连接脚本.

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
and save to run this script repeatedly every minute. Use `crontab -l` to confirm the configuration file is saved.

### 使用方法

* `./connect.py --gen-config`: 生成配置文件.
* `./connect.py --connect`   : 直接连接.
* `./connect.py --test-first`: 先测试网络, 不通再连接.

首先用 `./connect.py --gen-config` 按提示输入用户名密码生成配置文件, 之后用 `./connect.py --connect` 或 `./connect.py --test-first` 连接.

### 亮点

* 更短, 所以更少的八阿哥.
* 可以先测试网络是否通畅失败才重连.
* 保存密码的哈希而不是明文.

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
并且保存退出来让脚本每分钟重复执行。使用`crontab -l`确认配置被保存了。
