#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
call a shell command
"""
import subprocess
from subprocess import PIPE
import shlex

def call(cmd, output=PIPE):
    """ call a command string """
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=output, stderr=output)
    out, err = p.communicate()
    return (p.returncode, out, err)

def runPipe(cmds):
    try: 
        p1 = subprocess.Popen(shlex.split(cmds[0]), stdin=None, stdout=PIPE, stderr=PIPE)
        prev = p1
        for cmd in cmds[1:]:
            p = subprocess.Popen(shlex.split(cmd), stdin=prev.stdout, stdout=PIPE, stderr=PIPE)
            prev = p
        stdout, stderr = p.communicate()
        p.wait()
        returncode = p.returncode
    except Exception, e:
        stderr = str(e)
        returncode = -1
    if returncode == 0:
        return (True, stdout)
    else:
        return (False, stderr)