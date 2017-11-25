#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
build progress
"""

import os
import sys
import datetime
import shutil
from optparse import OptionParser
import config
import build_ipa
import filter_log
import mail
import fir
import bugly
import dingtalk_bot
import date_format
import git
import resign

def build_if_need():
    git_info = config.config_dic['git']

    project_path = config.config_dic['project_path']

    branch = 'master'
    current_branch = git.get_current_branch(project_path)
    if current_branch:
        branch = current_branch

    if git_info['pull_before_build']:
        print('Pulling latest code...')

        if git_info['branch']:
            if git_info['branch'] == branch:
                git.pull(project_path, branch=branch)
            else:
                git.checkout_and_pull(project_path, branch=git_info['branch'])
        else:
            git.pull(project_path, branch=branch)

        print('Pull code complete!')

    current_commit = git.get_current_commit(project_path)

    last_try_file = config.config_dic['log_path'] + 'last_try_build.txt'
    last_build_file = config.config_dic['log_path'] + 'last_build.txt'

    last_try_commit = '0'
    last_build_commit = '0'

    if os.path.exists(last_try_file):
        with open(last_try_file, 'r') as f:
            last_try_commit = f.read()

    if os.path.exists(last_build_file):
        with open(last_build_file, 'r') as f:
            last_build_commit = f.read()

    if last_try_commit == current_commit:
        print('Build have tried, exit!')
        return (False, None)

    commit_msg = git.get_latest_commit_msg(project_path)

    build_target = None
    for key in config.config_dic['build']:
        if config.config_dic['build'][key]['build_identifier'] in commit_msg:
            build_target = key
            break

    if not build_target:
        print('No build identifier, exit!')
        return (False, None)
    
    if last_build_commit == current_commit:
        print('This build has been builded, exit!')
        return (False, None)

    print('Build identifier detect, build start...')
    print('Build info {}'.format(config.config_dic['build'][build_target]))
    return (True, build_target)

def build_and_upload(build_target):
    build_info = config.config_dic['build'][build_target]
    print('Building...')
    build_res = build_ipa.build_ipa(build_target)

    resign_info = build_info['resign']
    if resign_info['enable']:
        resign_res = resign.resign(build_res[2], build_info)
        if resign_res[0] == 0:
            build_res = (build_res[0], build_res[1], resign_res[1])
        else:
            build_res = (1, None, None)
            return build_res

    if build_res[0] != 0:
        print('Build failure!')
        failture_mail_info = config.config_dic['email_after_failure']
        if failture_mail_info['enable']:
            mail.send_failture_msg('Build failure!', build_target)
    else:
        print('Build success!')
        cp_info = config.config_dic['copy_to']
        if cp_info['enable']:
            path = cp_info['path']
            if not os.path.exists(path):
                os.mkdir(path)
            shutil.copy(build_res[2], path)
            print('Copy to {}'.format(path))
        
        fir_info = config.config_dic['upload_to_fir']
        if  fir_info['enable']:
            print('Upload to fir.im...')
            fir.upload(fir_info['path'], build_res[2], fir_info['token'])
            print('Upload complete!')

        bugly_info = config.config_dic['bugly']
        if bugly_info['enable']:
            print('Upload symbol file to bugly...')
            bugly.upload(build_res[1], build_info)
            print('Upload complete!')
    return build_res

def build(build_target, send_msg=True):
    last_try_file = config.config_dic['log_path'] + 'last_try_build.txt'
    last_build_file = config.config_dic['log_path'] + 'last_build.txt'

    with open(last_build_file, 'r') as f:
        last_build_commit = f.read()

    current_commit = git.get_current_commit(config.config_dic['project_path'])

    with open(last_try_file, 'w') as f:
        f.write(current_commit)

    build_res = build_and_upload(build_target)

    if build_res[0] == 0:
        with open(last_build_file, 'w') as f:
            f.write(current_commit)

        if send_msg:
            mail_info = config.config_dic['email_after_build']
            if mail_info['enable']:
                print('Send email...')
                if mail_info['send_filter_log']:
                    log = filter_log.msg_with_intall_info(last_build_commit, build_target)
                    mail.send_success_msg(log, build_target)
                else:
                    mail.send_success_msg("Build success!", build_target)
                print('Send complete!')
            
            ding_info = config.config_dic['send_ding_msg_after_build']
            if ding_info['enable']:
                print('Send dingtalk message...')
                tokens = ding_info['tokens']
                title = mail.get_subject(build_target)
                if ding_info['send_filter_log']:
                    log = title + '\n\n' + filter_log.msg_with_intall_info(last_build_commit, build_target)
                    dingtalk_bot.sendMessage(log, tokens)
                else:
                    dingtalk_bot.sendMessage(title + '\n\n' + '打包成功!', tokens)
                print('Send complete!')

    print('Build complete!')

if __name__ == "__main__":
    print('-------------------------- Launch Script --------------------------')
    start_time = datetime.datetime.now()
    print('Start time {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage)
    parser.add_option("-c", "--config", dest='config', help='config file path')
    parser.add_option("-a", "--auto", dest='auto', action='store_true', help='use auto mode, defalut False, you must set target option with valid value when defalut value', default=False)
    parser.add_option("-t", "--target", dest='target', help='build target, will be ignored when auto option is True')
    (options, args) = parser.parse_args()
    config_file = options.config
    auto = options.auto
    target = options.target

    if not config:
        print('You must set a config file path!')
        sys.exit(1)

    if (not auto) and (not target):
        print('You must set a build target!')
        sys.exit(1)
    config.init(config_file)

    if auto:
        build_if = build_if_need()
        if build_if[0]:
            build(build_if[1])
    else:
        build_and_upload(target)
    print('Finish time {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('Total time {}'.format(date_format.strfdelta(datetime.datetime.now() - start_time, "%H hours %M mins %S seconds")))
    # try:
    # except:
    #     sys.exit(0)

