# Tsinghua Tunet auto-connect script.
## 清华校园网自动连接脚本.

### Usage

* `./connect.py --gen-config`: Generate a configure file including your username and password's hash.
* `./connect.py --connect`   : Connect directly.
* `./connect.py --test-first`: First test network by getting a PKU webpage, connect if failed.

First, use `./connect.py --gen-config` to generate a configure file. Then try `./connect.py --connect` or `./connect.py --test-first`.

### Feature

* Short so fewer bugs.
* Able to test network and reconnect if the test fails.
* Save password's hash rather than plaintext.

### 使用方法

* `./connect.py --gen-config`: 生成配置文件.
* `./connect.py --connect`   : 直接连接.
* `./connect.py --test-first`: 先测试网络, 不通再连接.

首先用 `./connect.py --gen-config` 按提示输入用户名密码生成配置文件, 之后用 `./connect.py --connect` 或 `./connect.py --test-first` 连接.

### 亮点

* 更短, 所以更少的八阿哥.
* 可以先测试网络是否通畅失败才重连.
* 保存密码的哈希而不是明文.
