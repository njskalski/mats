# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this file is a temporary wrap-up for dev purposes

from sys import argv, stdout
from optparse import OptionParser
from mats_runner import MatsRunner

parser = OptionParser()
parser.add_option('-c', '--config',
                  dest='config',
                  help="alternative config file location",
                  metavar="FILE",
                  default="config.ini")

args = parser.parse_args()
print 'Using config file: ' + args[0].config

runner = MatsRunner(args[0].config)