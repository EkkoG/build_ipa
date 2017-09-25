A build tool use automation build ipa and distrabution to test.

### Feature

- Pull code scheduled, build depend on lastest Git commit message
- Pull code before build
- Filter log between two build
- Upload IPA to fir.im after build succces
- Upload symbol file to bugly after build succces
- Copy to somewhere after build succces
- Send mail after build success(optional you can send filter log)
- Send Dingtalk message after build success(optional you can send filter log)
- Send mail after build failure, build log as attachment
- Optional you can use the tool manual, only upload to fir.im and bulgy support

### Requirement

- xcodebuild tool insatlled
- Python3
- Git
- fir gem
- bugly jar file and Java installed

This tool only support python3, and it has several platform tool dependency, you should install them manually.

### Usage

There is a config example, use YAML format

```
# ===========================================
# Build config file
# ===========================================

# Project path, absolute path
project_path: 'path log project'
# Workspace name, file name under project path
worspace_name: 'Example.xcworkspace'
# Log path, absolute path
log_path: 'path of log'
# Build file (archive, ipa etc) path, absolute path
builds_path: 'path of builds, for IPA'
# Build log file name, build log located in builds_path's log folder
builg_log: build.log

# Git info
git:
  pull_before_build: true
  # Which branch to build, if not set, will use the local repo's current brach
  branch: 

# Dingtalk preferences
send_ding_msg_after_build:
  enable: false
  # Dingtalks tokens to send message
  tokens: 
    - cbd71be588ejldjaf232311b2551ad6dae09b47549aef7e2dd513d906d64c77a
    - 736df1d522fee3f7cc29d0joalfja11sll4df9351589be32d7dfabca7637677d
  # Option send filter log
  send_filter_log: true

# Filter info, use to fileter log
filter_log:
  prefix: "["

# Fir info
upload_to_fir:
  enable: true
  # custom fir path
  path: '/usr/local/bin/fir'
  token: 7lkjljlkaaab0ed4322a685c1d61f

# Copy ipa to path
copy_to:
  enable: true
  # Path to copy, absolute path
  path: 'path to copy'

# Bugly info
bugly:
  enable: true
  # Jar file location, absolute path
  jar_file: 'file path of bugly Jar file'

# Mail login info, must suppport ssl login
mail_info:
  server: smtp.example.com
  user: admin@example.com
  password: password

# Mail preferences
email_after_build:
  enable: true
  # Option send filter log
  send_filter_log: true
  # Mail receiver
  send_to: 
    # - lifanghao@dasheng.tv
    - send_to@example.com
  # Mail cc to
  cc_to: 
    - cc_to@example.com

# Mail preferences when build failure
email_after_failure:
  enable: false
  # Mail receiver
  send_to: 
    - send_to@example.com
  cc_to: 
    - cc_to@example.com
  cc_to: 

# Build info, dictionary
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
    # Identifier use to detect a build, must unique among all build info
    build_identifier: BUILDIPA
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

Usage example

```
path/to/python3 -c path/to/config -t 'dev'
```

### WARMING!

It's recomment use auto mode with launchctl, there has two benifit

1. launchctl environment can aceess login keychain, THIS IS A HUGE BENIFIT, you can save many time deal the cetificate issue.
2. launchctl run one instance at a time, you do not need warry about to many install run at same time.

