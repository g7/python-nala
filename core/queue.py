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

from gi.repository import GObject, GLib

class Queue(GObject.GObject):
	""" Handles the rebuild queue. 
	
	How the Queue works:
	- An Application(), added via self.add_application(), is linked
	  on every trigger it requires.
	- When something occours, self.add_to_queue() needs to be called.
	  This may be done by connecting the "watcher-changed" signal of the
	  WatcherPool or the "changed" signal of the Watcher to a dummy
	  method which calls the appropriate queue's add_to_queue().
	- self.add_to_queue() takes note of the event and sets a timeout of
	  3 seconds (default, can be changed when constructing the class using
	  the wait_time argument) before telling listeners to do the things
	  they want.
	- If another event happens BEFORE the 3 seconds timeout, the timeout
	  is resetted.
	  This *may* be an issue if you want to work on directories like /tmp,
	  so you need to set the wait_time to 0 in that case.
	- If after the timeout everything is good, the object automatically
	  merges reported events (e.g. handling a 'changed' event when
	  a file has been deleted later has no sense) and fires the
	  "processable" signal.
	  """
	
	__gsignals__ = {
		"processable" : (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_PYOBJECT,))
	}
		
	in_queue = []
	triggers = {}
	timeout = None

	def __init__(self, wait_time=3):
		""" Initializes the Queue object.
		
		wait_time is the time (in seconds) the Queue should wait
		before emit the processable signals. """

		GObject.GObject.__init__(self)

		self.wait_time = wait_time
		#self.timer = GLib.Timer()

	def add_application(self, app):
		""" Adds an Application. """
		
		for trigger in app.triggers:
			if not trigger in self.triggers:
				self.triggers[trigger] = []
			
			self.triggers[trigger].append(app)
	
	def __processable(self, override=None):
		""" When this method is fired, we are almost ready to hand-off 
		the current Queue to the listeners of the 'processable' signal. """
		
		if not override:
			self.emit("processable", self.in_queue)
			self.in_queue = []
		else:
			self.emit("processable", override)
		
		# Remove the timeout
		if self.timeout:
			GLib.source_remove(self.timeout)
			self.timeout = None
	
	def add_to_queue(self, watcher, trigger, event):
		""" Adds a trigger to the queue. """
		
		if self.timeout:
			# An existing timeout is there, we need to delete it...
			GLib.source_remove(self.timeout)
		
		trigger_path = trigger.get_path()
		
		if not watcher.path in self.triggers:
			# We do not need to touch this
			return
		
		if self.wait_time > 0:
			self.in_queue.append((watcher.path, trigger_path, event))
			self.timeout = GLib.timeout_add_seconds(self.wait_time, self.__processable)
		else:
			# We need to ensure to fire a processable signal for every
			# add_to_queue call, so using a global list is not reliable.
			# We pass the items directly to self.__processable
			GObject.idle_add(self.__processable, (watcher.path, trigger_path, event))
