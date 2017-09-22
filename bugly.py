#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
upload symbol file to bugly
"""

from call_cmd import call
import config

def upload(archive=None, build_info=None):
    bugly_info = config.config_dic['bugly']

    dSYM_path = "{}/dSYMs/{}.app.dSYM".format(archive, build_info['scheme'])
    version = call('''/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" {}'''.format(config.config_dic['project_path'] + build_info['info_plist']))[1]

    cmd = "java -jar {} -i {} -u -id {} -key {} -package {} -version {}".format(bugly_info['jar_file'], dSYM_path, build_info['bugly_id'], build_info['bugly_key'], build_info['bundle_id'], version)
    return call(cmd)