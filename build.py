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
import shutil
from call_cmd import call
import config
import build_ipa
import filter_log
import mail
import fir
import bugly
import dingtalk_bot

if __name__ == "__main__":

    config.init('/Users/ciel/Documents/build.yaml')

    build_target = 'dev'
    build_info = config.config_dic['build'][build_target]

    git_info = config.config_dic['git']
    print '更新代码...'
    if git_info['pull_before_build']:
        if git_info['branch']:
            call('git -C {} checkout {}'.format(config.config_dic['project_path'], git_info['branch']))
        call('git -C {} pull'.format(git_info['branch']))

    print '更新代码完成!'
    print '开始打包...'
    build_res = build_ipa.build_ipa(build_target)
    if build_res[0] != 0:
        print '打包失败!'
        failture_mail_info = config.config_dic['email_after_failture']
        if failture_mail_info['enable']:
            mail.send_failture_msg('打包失败!', build_target)
    else:
        print '打包成功!'
        cp_info = config.config_dic['copy_to']
        if cp_info['enable']:
            path = cp_info['path']
            if not os.path.exists(path):
                os.mkdir(path)
            shutil.copy(build_res[2], path)
            print '复制到 {}'.format(path)
        
        fir_info = config.config_dic['upload_to_fir']
        if  fir_info['enable']:
            print '开始上传到 fir.im...'
            fir.upload(build_res[2], fir_info['token'])
            print '上传完成!'

        bugly_info = config.config_dic['bugly']
        if bugly_info['enable']:
            print '开始上传符号文件...'
            bugly.upload(build_res[1], build_info)
            print '上传成功!'

        mail_info = config.config_dic['email_after_build']
        if mail_info['enable']:
            print '发送 email...'
            if mail_info['send_filter_log']:
                log = filter_log.msg_with_intall_info('782d124', build_target)
                mail.send_success_msg(log, build_target)
            else:
                mail.send_success_msg("打包成功!", build_target)
            print '发送完成!'
        
        ding_info = config.config_dic['send_ding_msg_after_build']
        if ding_info['enable']:
            print '发送钉钉消息...'
            tokens = ding_info['tokens']
            if ding_info['send_filter_log']:
                log = filter_log.msg_with_intall_info('782d124', build_target)
                dingtalk_bot.sendMessage(log, tokens)
            else:
                dingtalk_bot.sendMessage('打包成功!', tokens)
            print '发送完成!'

    print '打包完毕!'