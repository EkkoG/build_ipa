#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
date format
"""

from string import Template

class DeltaTemplate(Template):
    delimiter = '%'

def strfdelta(tdelta, fmt):
    d = {}
    l = {'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    rem = int(tdelta.seconds)

    for k in ( 'D', 'H', 'M', 'S' ):
        if "%{}".format(k) in fmt:
            d[k], rem = divmod(rem, l[k])

    t = DeltaTemplate(fmt)
    return t.substitute(**d)
