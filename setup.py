#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# nala - file/directory watcher
# Copyright (C) 2013  Eugenio "g7" Paolantonio <me@medesimo.eu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from distutils.core import setup

setup(name='nala',
	version='0.0.1',
	description='file/directory watcher libraries',
	author='Eugenio Paolantonio',
	author_email='me@medesimo.eu',
	url='https://github.com/g7/python-nala',
	packages=[
		"nala"
      ],
	requires=['gi.repository.GLib', 'gi.repository.GObject', 'gi.repository.Gio']
)

