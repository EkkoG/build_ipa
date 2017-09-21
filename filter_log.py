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

from call_cmd import call, runPipe
import config
import time
import os

def filter_log(last_commit):
    git_logs_cmd = '''git -C {} log --pretty=\"%s\" {}..HEAD'''.format(config.config_dic['project_path'], last_commit)
    logs = call(git_logs_cmd)

    log_has_prefix = []

    prefix = config.config_dic['filter_log']['prefix']
    if not prefix:
        prefix = '['

    for line in logs[1].split("\n"):
        if line.startswith(prefix):
            log_has_prefix.append(line)

    if not log_has_prefix[1]:
        return None

    log_file = '{}log.txt'.format(config.config_dic['builds_path'])

    with open(log_file, 'w') as f:
        for line in log_has_prefix:
            f.write('{}\n'.format(line))

    with open(log_file, 'r+') as f:
        flip_cmd = "sed '1!G;h;$!d' " + log_file
        res = call(flip_cmd)
        f.write(res[1])

    with open(log_file, 'r+') as f:
        add_num_cmd = """awk '{printf NR"."" "}1' """ + log_file
        res = call(add_num_cmd)
        f.write(res[1])

    with open(log_file, 'r') as f:
        return f.read()


