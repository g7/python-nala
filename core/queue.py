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
# This file contains the queue library.

from gi.repository import GObject

class Queue(GObject.GObject):
	""" Handles the rebuild queue. """
	
	# Hey, this needs implementation!
	
	in_queue = []
	in_build = []
	triggers = {}

	def add_application(self, app):
		""" Adds an Application. """
		
		for trigger in app.triggers:
			if not trigger in self.triggers:
				self.triggers[trigger] = []
			
			self.triggers[trigger].append(app)
	
	def add_to_queue(self, watcher, trigger, event):
		""" Adds a trigger to the queue. """
		
		trigger_path = trigger.get_path()
		
		if not watcher.path in self.triggers:
			# We do not need to touch this
			return
		
		self.in_queue.append((watcher.path, trigger_path, event))
