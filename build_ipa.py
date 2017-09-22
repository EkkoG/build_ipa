#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ciel <ciel@cieldeMBP>
#
# Distributed under terms of the MIT license.

"""
build ipa
"""

import os
from call_cmd import call

import config

def build_ipa(target=None):
    build_info = config.config_dic['build'][target]

    scheme_name = build_info['scheme']
    archive_path = config.config_dic['builds_path'] + scheme_name + '.xcarchive'

    archive_cmd = "xcodebuild archive -workspace {} -scheme {} -archivePath {} ONLY_ACTIVE_ARCH=NO TARGETED_DEVICE_FAMILY=1 -allowProvisioningUpdates".format(config.config_dic['project_path'] + config.config_dic['worspace_name'], scheme_name, archive_path)
    log_file = config.config_dic['builds_path'] + config.config_dic['builg_log']
    file = open(log_file, 'w+')
    res = call(archive_cmd, file)

    if res[0] != 0:
        return (1, None, None)

    export_plist_template = """
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>compileBitcode</key>
        <false/>
        <key>method</key>
        <string>{}</string>
        <key>provisioningProfiles</key>
        <dict>
            <key>{}</key>
            <string>{}</string>
        </dict>
        <key>signingCertificate</key>
        <string>iPhone Developer</string>
        <key>signingStyle</key>
        <string>manual</string>
        <key>stripSwiftSymbols</key>
        <true/>
        <key>teamID</key>
        <string>{}</string>
        <key>thinning</key>
        <string>&lt;none&gt;</string>
    </dict>
    </plist>
    """
    export_plist = export_plist_template.format(build_info['export_mothod'], build_info['bundle_id'], build_info['provisioning_profile'], build_info['team_id'])
    export_plist_path = config.config_dic["builds_path"] + "export.plist"

    with open(export_plist_path, 'w') as f:
        f.write(export_plist)

    export_cmd = "xcodebuild -exportArchive -archivePath {} -exportOptionsPlist {} -exportPath {} -allowProvisioningUpdates".format(archive_path, export_plist_path, config.config_dic['builds_path'])
    res = call(export_cmd, file)

    if res[0] != 0:
        return [1, None, None ]

    ipa_path = config.config_dic["builds_path"] + scheme_name + '.ipa'
    
    if not os.path.exists(ipa_path):
        return [1, None, None ]

    file.close
    return [0, archive_path,  ipa_path]

if __name__ == "__main__":
    build_ipa()