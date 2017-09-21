#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
send mail
"""

from sender import Mail
from sender import Message
import config
from call_cmd import call

def send(text, subject=None, cc=None, to=None):
    mail_info = config.config_dic['mail_info']
    sendEmail(mail_info, mail_info['user'], to, subject, text, cc)

def send_success_msg(text, build):
    to_user_info = config.config_dic['email_after_build']
    if not to_user_info['enable']:
        return
    send(text, get_subject(build), to_user_info['send_to'], to_user_info['cc_to'])

def send_success_msg(text, build):
    to_user_info = config.config_dic['email_after_failture']
    if not to_user_info['enable']:
        return
    send("打包失败!", get_subject(build), to_user_info['send_to'], to_user_info['cc_to'])

def get_subject(build):
    build_info = config.config_dic['build'][build]
    version = call('''/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" {}'''.format(config.config_dic['project_path'] +build_info['info_plist']))[1]
    build_version = call('''/usr/libexec/PlistBuddy -c "Print CFBundleVersion" {}'''.format(config.config_dic['project_path'] + build_info['info_plist']))[1]
    subject = build_info['app_name'] + ' ' + str.strip(version) + ' ' + 'Build' + ' ' + str.strip(build_version)
    return subject


def sendEmail(authInfo, fromAdd, toAdd, subject, content, cc=None):
    sslPort = 465
    server = authInfo.get('server')
    user = authInfo.get('user')
    passwd = authInfo.get('password')

    if not (server and user and passwd):
        print ('incomplete login info, exit now')
        return

    mail = Mail(server, port=sslPort, username=user, password=passwd,
                use_tls=False, use_ssl=True, debug_level=None)
    msg = Message(subject)
    msg.fromaddr = (user, user)
    msg.to = toAdd
    if cc:
        msg.cc = cc 
    msg.body = content
    msg.charset = "utf-8"
    mail.send(msg)