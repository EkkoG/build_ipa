#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
filter git log
"""

import codecs
from call_cmd import call
import config

def filter_log(last_commit):
    commit_valid = call('git -C {} cat-file -e '.format(config.config_dic['project_path']) + last_commit)[0]
    if commit_valid != 0:
        return '无'

    git_logs_cmd = '''git -C {} log --pretty=\"%s\" {}..HEAD'''.format(config.config_dic['project_path'], last_commit)
    logs = call(git_logs_cmd)

    log_has_prefix = []

    prefix = config.config_dic['filter_log']['prefix']
    if not prefix:
        prefix = '['

    for line in logs[1].split("\n"):
        if line.startswith(prefix):
            log_has_prefix.append(line)

    if log_has_prefix.count:
        return '无'

    log_file = '{}log.txt'.format(config.config_dic['builds_path'])

    with codecs.open(log_file, 'w', 'UTF-8') as f:
        for line in log_has_prefix:
            f.write('{}\n'.format(line))

    with codecs.open(log_file, 'r+', 'UTF-8') as f:
        flip_cmd = "sed '1!G;h;$!d' " + log_file
        res = call(flip_cmd)
        f.write(res[1])

    with codecs.open(log_file, 'r+', 'UTF-8') as f:
        add_num_cmd = """awk '{printf NR"."" "}1' """ + log_file
        res = call(add_num_cmd)
        f.write(res[1])

    with codecs.open(log_file, 'r', 'UTF-8') as f:
        return f.read()


def msg_with_intall_info(last_commit, build):
    build_info = config.config_dic['build'][build]
    log = filter_log(last_commit)

    msg = '更新日志:' + '\n\n' + log + '\n\n' + '安装地址：' + build_info['download_url']
    return msg