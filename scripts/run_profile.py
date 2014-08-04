#!/usr/bin/python3

# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2014 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Profile qutebrowser."""

import sys
import cProfile
import os.path
from os import getcwd
from tempfile import mkdtemp
from subprocess import call
from shutil import rmtree

sys.path.insert(0, getcwd())

import qutebrowser.qutebrowser  # pylint: disable=unused-import

tempdir = mkdtemp()

if '--profile-keep' in sys.argv:
    sys.argv.remove('--profile-keep')
    profilefile = os.path.join(getcwd(), 'profile')
else:
    profilefile = os.path.join(tempdir, 'profile')
if '--profile-noconv' in sys.argv:
    sys.argv.remove('--profile-noconv')
    noconv = True
else:
    noconv = False

callgraphfile = os.path.join(tempdir, 'callgraph')
profiler = cProfile.Profile()
profiler.run('qutebrowser.qutebrowser.main()')
profiler.dump_stats(profilefile)

if not noconv:
    call(['pyprof2calltree', '-k', '-i', profilefile, '-o', callgraphfile])
rmtree(tempdir)
