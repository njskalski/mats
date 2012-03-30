# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

def get_config(config_file = "../config.ini"):
    from ConfigParser import ConfigParser
    
    config = ConfigParser()
    config.read(config_file)
    
    #line below creates function res: section -> key -> value (haskell notation) 
    res = { section : { a : b for (a,b) in config.items(section) } for section in config.sections() }
    return res