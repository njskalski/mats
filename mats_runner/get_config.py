# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#This file provides a get_config function, that either succeeds or raise the exception.
#If it succeeds, it returns a dictionary of settings, in which following requirements are met:
#
#- conf['Firefox'] section exists
#- conf['Firefox']['binary'] exists and points to an existing file
#- conf['Marionette'] section exists
#- conf['Marionette']['port'] exists and is positive, integer type
#- conf['Marionette']['port_timeout'] exists and is positive, integer type

defaultMarionettePort = 2828
defaultMarionettePortTimeout = 300

defaults = {
    'Marionette' : {
        'port' : 2828,
        'port_timeout' : 300
                    }
            }

def test_and_fill(conf):
    '''
    method fills missing fields in config, and types present correctly. All int's are to be positive.
    '''
    
    for section in defaults.keys():
        if section in conf.keys():
            for field in defaults[section].keys():
                if field in conf[section].keys():
                    conf[section][field] = defaults[section][field].__class__(conf[section][field])
                    if conf[section][field].__class__ == int:
                        if not conf[section][field] > 0:
                            raise Exception('Setting "' + field + '" in section "' + section + ' is non-positive.')
                else:
                    conf[section][field] = defaults[section][field]
        else:
            conf[section] = defaults[section] 

def get_config(config_file):
    from ConfigParser import ConfigParser
    from os import path
    
    config = ConfigParser()
    config.read(config_file)
    
    #line below creates dictionary conf: section -> key -> value  
    conf = { section : { a : b for (a,b) in config.items(section) } for section in config.sections() }
    
    #testing for Firefox/Nightly binary being specified and present
    if 'Firefox' not in conf.keys():
        raise Exception('Could not find "Firefox" section in "' + config_file + '".')
    if 'binary' not in conf['Firefox'].keys():
        raise Exception('Could not find "binary" setting in Firefox section in "' + config_file + '".')
    if not path.exists(conf['Firefox']['binary']):
        raise Exception('Path to binary: "' + conf['Firefox']['binary'] + '" is incorrect.')
    
    #testing all other settings against defaults
    test_and_fill(conf)
    
    return conf
