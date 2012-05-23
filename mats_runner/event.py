# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

class Event(object):
    '''
    This is a wrapper class for events returned from event loop.
    '''
    
    def __init__(self, id, *args, **kwargs):
        self.id = id
        #since I don't have idea what to do with some fields now
        self.args = args
        self.kwargs = kwargs
        
    def get_id(self):
        return self.id 
    
    def __str__(self):
        return 'Event object id:' + str(self.id) + '\nargs:\n' + str(self.args) + '\nkwargs:\n' + str(self.kwargs)