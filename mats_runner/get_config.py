# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

def get_config(config_file):
    from ConfigParser import ConfigParser
    from os import path
    
    config = ConfigParser()
    config.read(config_file)
    
    #line below creates dictionary conf: section -> key -> value  
    conf = { section : { a : b for (a,b) in config.items(section) } for section in config.sections() }
    
    #do that if you don't get the config format
    #print conf
    
    if not 'Firefox' in conf.keys():
        raise Exception('Could not find "Firefox" section in "' + config_file + '".')
    
    if not 'binary' in conf['Firefox'].keys():
        raise Exception('Could not find "binary" setting in Firefox section in "' + config_file + '".')
    
    if not path.exists(conf['Firefox']['binary']):
        raise Exception('Path to binary: "' + conf['Firefox']['binary'] + '" is incorrect.')
    
    return conf