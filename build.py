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

from call_cmd import call, runPipe
import config
import build_ipa
import filter_log
import mail

if __name__ == "__main__":
    config.init('/Users/ciel/Documents/build.yaml')

    log = filter_log.filter_log('782d124')
    print(log)
    # mail.send_success_msg(log, 'dev')

#    build_ipa.build_ipa('dev')
