一个可以自动打包和发布测试的工具

### 特性

- 定时拉取代码，根据 git commit message 来决定是否打包
- 打包前拉取最新代码
- 过滤两次打包间的 git 日志
- 打包成功后更新到 fir.im
- 打包成功后上传符号文件到 bugly
- 复制 ipa 到某个地方
- 打包成功后发送邮件（可选是否发送 git 日志）
- 打包成功后发送钉钉消息（可选是否发送 git 日志）
- 打包失败后发送邮件，附带打包日志
- 可手动使用，只上传到 fir.im 和符号文件

### 依赖的工具

- Xcode 9
- Python3
- Git
- fir gem
- bugly jar 文件和 Java 环境

本工具只支持 Python3，并依赖几个工具，你必须手动安装它们

### 在新电脑上需要配置的东西

1. 安装 Xcode 9
2. 安装 python3
3. 安装 Java 运行时环境 (下载 JDK 并安装)
4. 安装 fir-cli
5. 测试手动打包是否成功运行
6. 添加计划任务（如果需要）

### 使用方法

First you should install the python dependencies
首先需要安装 Python 模块

```
git clone https://github.com/cielpy/build_ipa.git
cd build_ipa
[sudo]pip3 install -r requirements.txt
```

```
Usage: build.py [options] arg

Options:
  -h, --help            show this help message and exit
  -c CONFIG, --config=CONFIG
                        config file path
  -a, --auto            use auto mode, defalut False, you must set target
                        option with valid value when defalut value
  -t TARGET, --target=TARGET
                        build target, will be ignored when auto option is True
```

使用示例

```
path/to/python3 path/to/build.py -c path/to/config -t 'dev'
```

以下是一个配置文件示例，使用 YAML 格式

``` yaml
# ===========================================
# 打包配置文件
# ===========================================

# 项目路径（绝对路径）
project_path: 'path log project'
# 项目目录下的 Workspace 名字
worspace_name: 'Example.xcworkspace'
# 日志保存路径（绝对路径）
log_path: 'path of log'
# IPA 保存路径（绝对路径）
builds_path: 'path of builds, for IPA'
# 日志文件名，相对于 builds_path 的路径
builg_log: build.log

# Git 相关信息
git:
  # 是否开启打包前拉取代码
  pull_before_build: true
  # 需要打包的分支，如果未设定，则会使用工程的当前分支
  branch: 

# 钉钉配置
send_ding_msg_after_build:
  enable: false
  # token 数组，收集需要消息的群的 token
  tokens: 
    - cbd71be588ejldjaf232311b2551ad6dae09b47549aef7e2dd513d906d64c77a
    - 736df1d522fee3f7cc29d0joalfja11sll4df9351589be32d7dfabca7637677d
  # 是否发送过滤好的日志
  send_filter_log: true

# 日志过滤信息
filter_log:
  # 日志的前缀
  prefix: "["

# fir.im 配置
upload_to_fir:
  enable: true
  # fir-cli 路径
  path: '/usr/local/bin/fir'
  token: 7lkjljlkaaab0ed4322a685c1d61f

# 复制信息
copy_to:
  enable: true
  # 打包成功后复制到的路径
  path: 'path to copy'

# Bugly 配置
bugly:
  enable: true
  # Jar 文件路径（绝对路径）
  jar_file: 'file path of bugly Jar file'

# 电子邮件登录信息，须支持 SSL 登录
mail_info:
  server: smtp.example.com
  user: admin@example.com
  password: password

# 电子邮件配置，打包成功后
email_after_build:
  enable: true
  # 是否发送过滤的日志
  send_filter_log: true
  # 邮件接收者
  send_to: 
    - send_to@example.com
  # 邮件需要抄送的人
  cc_to: 
    - cc_to@example.com

# 打包失败后邮件配置
email_after_failure:
  enable: false
  # 邮件接收者
  send_to: 
    - send_to@example.com
  cc_to: 
    - cc_to@example.com
  cc_to: 

# 打包配置
build:
  dev: 
    info_plist: Example/Info.plist
    bugly_key: cac0689a-lkkk-11212-a120-4e0118f8d462
    bugly_id: i1400012222
    download_url: https://fir.im/abcd
    app_name: Example
    team_id: JLKJJ3333
    export_mothod: development
    scheme: Example
    bundle_id: com.example
    provisioning_profile: 'iOS Development Dev'
    # Extra provisioning profile, use for project have extentions
    extra_provisioning_profile: 
      - bundle_id: com.example.extention
        provisioning_profile: 'iOS Development Dev Extention'
    resign:
      enable: true
      provisioning_profile: '/Users/xxx/Documents/xxx.mobileprovision'
      certificate: 'iPhone Distribution xxx Net Co., Ltd.'
      # Change app display nama
      app_name: 
      # Change bundle id, if not config, use provisioning profile's instead
      bundle_id:
      extentions:
        # Extentsion's scheme
        - scheme: xxx
          provisioning_profile: '/Users/xxx/Documents/xxx.mobileprovision'
          bundle_id:
    # Identifier use to detect a build, must unique among all build info
    build_identifier: BUILDIPA_DEV
  dis: 
    info_plist: Example/Info.plist
    bugly_key: jlkjlkjaa-7c5c-41e3-b54f-8dabd4c4da2b
    bugly_id: i1400111110
    download_url: https://fir.im/efgh
    app_name: Example-PROD
    team_id: JLKJLFDS11
    export_mothod: ad-hoc
    scheme: Example_PROD
    bundle_id: com.example.prod
    provisioning_profile: 'iOS Distribution Prod'
    # Identifier use to detect a build, must unique among all build info
    build_identifier: BUILDIPA_PROD
```

### WARMING!

It's recomment use auto mode with launchctl, there has two benifit

1. launchctl environment can aceess login keychain, THIS IS A HUGE BENIFIT, you can save many time deal the cetificate issue.
2. launchctl run one instance at a time, you do not need warry about to many install run at same time.
### 警告！

推荐使用 launchctl 来运行计划任务，有两个好处

1. launchctl 可以访问登录钥匙串
2. launchctl 自动处理多次打包情况，一次只运行一个任务


以下是一个 launchctl 的配置示例

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
    <dict>
        <key>EnvironmentVariables</key>
        <dict>
            <key>PATH</key>
            <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin</string>
            <key>PYTHONIOENCODING</key>
            <string>UTF-8</string>
        </dict>
        <key>Label</key>
        <string>com.cielpy.ipa</string>
        <key>ProgramArguments</key>
        <array>
            <string>/usr/local/bin/python3</string>
            <string>path/to/build.py</string>
            <string>-u</string>
            <string>-a</string>
            <string>-c</string>
            <string>path/to/build.yaml</string>
        </array>
        <key>RunAtLoad</key>
        <true />
        <key>StartInterval</key>
        <integer>60</integer>
        <key>StandardErrorPath</key>
        <string>/tmp/AlTest1.err</string>
        <key>StandardOutPath</key>
        <string>/tmp/AlTest1.out</string>
    </dict>
</plist>
```

Move it to `~/Library/LaunchAgents/` and run this command:

```
launchctl load ~/Library/LaunchAgents/com.cielpy.build_ipa.plist
```

Python 脚本将每 60s 运行一次，你可以自行修改。

配置完成后，你可以提交一个 commit，message 包含 `BUILDIPA` 字符串（在打包配置中设置），launchctl 将运行打包脚本并将 IPA 上传到第三方平台和其他操作。


