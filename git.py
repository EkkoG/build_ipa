#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
git operation
"""

from call_cmd import call

def get_current_branch(project_path):
    git_branches = call('git -C {} branch'.format(project_path))[1].splitlines()
    for line in git_branches:
        if line.startswith('*'):
            return line.split()[1]
    return None

def pull(project_path, repo='origin', branch='master'):
    call('git -C {} pull {} {}'.format(project_path, repo, branch))

def checkout_and_pull(project_path, repo='origin', branch='master'):
    call('git -C {} fetch {} {}'.format(project_path, repo, branch))
    call('git -C {} checkout {}'.format(project_path, branch))
    pull(project_path, repo, branch)

def get_current_commit(project_path):
    current_commit = call('''git -C {} --no-pager log --format="%H" -n 1'''.format(project_path))[1]
    return current_commit

def get_latest_commit_msg(project_path):
    commit_msg = call('''git -C {} --no-pager log --format="%s" -n 1'''.format(project_path))[1]
    return commit_msg