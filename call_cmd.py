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
    p = subprocess.Popen(args, stdin=None, stdout=output, stderr=output)
    out, err = p.communicate()
    if out:
        out = str.strip(out.decode('utf-8'))
    if err:
        err = str.strip(err.decode('utf-8'))
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
    except Exception as e:
        stderr = str(e)
        returncode = -1
    if returncode == 0:
        return (True, str.strip(stdout.decode('utf-8')))
    else:
        return (False, str.strip(stderr.decode('utf-8')))
