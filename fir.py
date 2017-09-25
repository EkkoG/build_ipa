#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
upload to fir
"""

from call_cmd import call

def upload(fir_path=None, ipa=None, token=None):
    upload_cmd = "{} p  {} -T {}".format(fir_path, ipa, token)
    return call(upload_cmd, None)
