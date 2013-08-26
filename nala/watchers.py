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
# This file contains the watchers library.

from gi.repository import Gio, GObject

class WatcherPool(GObject.GObject):
	""" A pool which handles multiple watchers. """
	
	__gsignals__ = {
		"watcher-changed" : (GObject.SIGNAL_RUN_LAST, None, (GObject.GObject, Gio.File, Gio.FileMonitorEvent,))
	}
	watchers = {}
		
	def add_watcher(self, paths):
		""" Creates a new Watcher and adds it to self.watchers. """
		
		if type(paths) not in (list,tuple): paths = (paths,)
		
		for path in paths:
			if path in self.watchers: continue
			
			self.watchers[path] = Watcher(path)
			self.watchers[path].connect("changed", self.on_child_watcher_changed)
	
	def on_child_watcher_changed(self, watcher, trigger, event):
		""" Triggered when a child watcher has been changed. """
		
		print event, trigger.get_path()
		
		# Also fire our own event to let listeners know...
		self.emit("watcher-changed", watcher, trigger, event)

class Watcher(GObject.GObject):
	""" A Watcher is that cool thingy which watches your file/directory to
	get any modifications happening there. """
	
	__gsignals__ = {
		"changed" : (GObject.SIGNAL_RUN_LAST, None, (Gio.File, Gio.FileMonitorEvent))
	}
	
	def __init__(self, path):
		""" Initializes watcher.
		
		path is the path to watch. """
		
		GObject.GObject.__init__(self)
		
		self.path = path
		self.file_object = Gio.File.new_for_path(self.path)
		self.file_monitor = self.file_object.monitor(Gio.FileMonitorFlags.NONE, None)
		
		self.file_monitor.connect("changed", self.on_changed)
		
	def on_changed(self, monitor, trigger, wtf, event):
		""" Triggered when the file or directory have been changed. """
		
		self.emit("changed", trigger, event)
