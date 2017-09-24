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
from sender import Attachment 
import config
from call_cmd import call

def send(text, subject=None, cc=None, toAdd=None, log_file=None):
    mail_info = config.config_dic['mail_info']
    sslPort = 465
    server = mail_info.get('server')
    user = mail_info.get('user')
    passwd = mail_info.get('password')

    if not (server and user and passwd):
        print ('Invalid login info, exit!')
        return

    mail = Mail(server, port=sslPort, username=user, password=passwd,
                use_tls=False, use_ssl=True, debug_level=None)
    msg = Message(subject)
    msg.fromaddr = (user, user)
    msg.to = toAdd
    if cc:
        msg.cc = cc 
    
    if log_file:
        with open(log_file) as f:
            attachment = Attachment("build.log", "text/plain", f.read())
            msg.attach(attachment)

    msg.body = text
    msg.charset = "utf-8"
    mail.send(msg)

def send_success_msg(text, build):
    to_user_info = config.config_dic['email_after_build']
    if not to_user_info['enable']:
        return
    send(text, get_subject(build), to_user_info['send_to'], to_user_info['cc_to'])

def send_failture_msg(text, build):
    to_user_info = config.config_dic['email_after_failture']
    if not to_user_info['enable']:
        return
    build_log = config.config_dic['log_path'] + config.config_dic['builg_log']
    send("Build failure!", get_subject(build), to_user_info['send_to'], to_user_info['cc_to'], build_log)

def get_subject(build):
    build_info = config.config_dic['build'][build]
    version = call('''/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" {}'''.format(config.config_dic['project_path'] + build_info['info_plist']))[1]
    build_version = call('''/usr/libexec/PlistBuddy -c "Print CFBundleVersion" {}'''.format(config.config_dic['project_path'] + build_info['info_plist']))[1]
    subject = build_info['app_name'] + ' ' + str.strip(version) + ' ' + 'Build' + ' ' + str.strip(build_version)
    return subject