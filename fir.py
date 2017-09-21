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

def upload(ipa=None, token=None):
    uplaod_cmd = "fir p  {} -T {}".format(ipa, token)
    return call(uplaod_cmd)
