# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#returns correct controller
#TODO: should I move it to constructor?
def get_controller():
    from platform import system
    osname = system()
    if osname == 'Linux':
        from mats_atspi_controller import MatsAtspiController
        controller = MatsAtspiController
    elif osname == 'Windows':
        from mats_msaa_controller import MatsMsaaController
        controller = MatsMsaaController
    else:
        raise Exception("Unsupported platform " + osname + ".")
    return controller()
