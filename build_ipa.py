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
import shutil
from call_cmd import call, runPipe

import config

def build_ipa(target=None):
    build_info = config.config_dic['build'][target]

    scheme_name = build_info['scheme']
    archive_path = config.config_dic['builds_path'] + scheme_name + '.xcarchive'

    archive_cmd = "xcodebuild archive -workspace {} -scheme {} -archivePath {} ONLY_ACTIVE_ARCH=NO TARGETED_DEVICE_FAMILY=1 -allowProvisioningUpdates".format(config.config_dic['project_path'] + config.config_dic['worspace_name'], scheme_name, archive_path)
    log_file = config.config_dic['log_path'] + config.config_dic['builg_log']
    file = open(log_file, 'w+')
    res = runPipe([archive_cmd, 'xcpretty'], file)

    if res[0] != 0:
        return (1, None, None)

    sign_certificate = 'iPhone Distribution'
    if build_info['export_mothod'] == 'development':
        sign_certificate = 'iPhone Developer'

    provisioning_profile_string = """
<key>{}</key>
<string>{}</string>
""".format(build_info['bundle_id'], build_info['provisioning_profile'])
    extra_provisinging_profiles = build_info['extra_provisioning_profile']
    for provisinging_profile in extra_provisinging_profiles:
        provisioning_profile_string += """
<key>{}</key>
<string>{}</string>
        """.format(provisinging_profile['bundle_id'], provisinging_profile['provisioning_profile'])

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
        {}
    </dict>
    <key>signingCertificate</key>
    <string>{}</string>
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
    export_plist = export_plist_template.format(build_info['export_mothod'], provisioning_profile_string, sign_certificate, build_info['team_id'])
    export_plist_path = config.config_dic["builds_path"] + "export.plist"

    with open(export_plist_path, 'w') as f:
        f.write(export_plist)

    export_cmd = "xcodebuild -exportArchive -archivePath {} -exportOptionsPlist {} -exportPath {} -allowProvisioningUpdates".format(archive_path, export_plist_path, config.config_dic['builds_path'])
    res = runPipe([export_cmd, 'xcpretty'], file)

    if res[0] != 0:
        return (1, None, None)

    version = call('''/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" {}'''.format(config.config_dic['project_path'] + build_info['info_plist']))[1]
    build_version = call('''/usr/libexec/PlistBuddy -c "Print CFBundleVersion" {}'''.format(config.config_dic['project_path'] + build_info['info_plist']))[1]

    ipa_name = '{}-{}-Build-{}.ipa'.format(scheme_name, str.strip(version), str.strip(build_version))

    ipa_path = config.config_dic["builds_path"] + ipa_name

    shutil.move(config.config_dic['builds_path'] + scheme_name + '.ipa', ipa_path)
    
    if not os.path.exists(ipa_path):
        return (1, None, None)

    file.close
    return (0, archive_path,  ipa_path)

if __name__ == "__main__":
    build_ipa()