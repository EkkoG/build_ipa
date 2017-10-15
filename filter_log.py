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

from call_cmd import call
import config

def filter_log(last_commit):
    commit_valid = call('git -C {} cat-file -e '.format(config.config_dic['project_path']) + last_commit)[0]
    if commit_valid != 0:
        return '无'

    git_logs_cmd = '''git -C {} log --pretty=\"%s\" {}..HEAD --reverse'''.format(config.config_dic['project_path'], last_commit)
    logs = call(git_logs_cmd)

    log_has_prefix = []

    prefix = config.config_dic['filter_log']['prefix']
    if not prefix:
        prefix = '['

    for line in logs[1].split("\n"):
        if line.startswith(prefix):
            log_has_prefix.append(line)

    if not log_has_prefix:
        return '无'

    log_text = ''
    i = 0
    while i < len(log_has_prefix):
        log_text += '{}.{}'.format(i + 1, log_has_prefix[i])
        if i < len(log_has_prefix) - 1:
            log_text += '\n'
        i += 1
                
    return log_text

def msg_with_intall_info(last_commit, build):
    build_info = config.config_dic['build'][build]
    log = filter_log(last_commit)

    msg = '更新日志:' + '\n\n' + log + '\n\n' + '安装地址：' + build_info['download_url']
    return msg