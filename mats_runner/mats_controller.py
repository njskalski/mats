# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from platform import system
osname = system()

if osname == 'Linux':
    from mats_atspi_controller import MatsAtspiController as MatsController
elif osname == 'Windows':
    #from mats_msaa_controller import MatsMsaaController as MatsController
    from mats_ia2_controller import MatsIA2Controller as MatsController
else:
    raise Exception("Unsupported platform " + osname + ".")

