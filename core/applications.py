#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# nala-watcher - file/directory watcher
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
# This file contains the applications library.

class Application:
	""" An Application object represents a target application which
	needs to do things when one of its watched files has been changed. """

	def __init__(self, path, triggers=[]):
		""" Constructs the object.
		
		path is the application's path.
		
		triggers is a list of trigger that will then become
		self.triggers.
		
		Note that an application trigger is not automatically added
		to the list of watched files.
		You need to update your WatcherPool accordingly. """
		
		self.path = path
		self.triggers = triggers
