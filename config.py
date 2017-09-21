#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
config service
"""

import yaml
import os

def init(file_path=None):
    global config_dic
    config_dic = read_config(file_path)
    valid_config(config_dic)
    make_path_valid(config_dic)

def read_config(path=None):
    """ read config from a file. """
    assert path != None, "file path cannot be none!"

    stream = file(path, 'r')
    return yaml.load(stream)

def valid_config(config=None):
    workspace_file_path = '{}{}'.format(config['project_path'], config['worspace_name'])
    return os.path.exists(config['project_path']) and os.path.exists(workspace_file_path)

def make_path_valid(config=None):
    if not os.path.exists(config['project_path']):
        os.makedirs(config['project_path'])

    if not os.path.exists(config['log_path']):
        os.makedirs(config['log_path'])
