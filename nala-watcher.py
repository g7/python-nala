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

from gi.repository import GLib

from nala.watchers import WatcherPool
from nala.queue import Queue
from nala.applications import Application

def on_incoming_queue(self, apps, lst):
	print "GOT QUEUE!", apps, lst

def add_to_queue(pool, watcher, trigger, event, queue):
	return queue.add_to_queue(watcher, trigger, event)

pool = WatcherPool()
queue = Queue(30)
xdgmenu = Application("/bin/echo", ["/usr/share/applications"])
pool.add_watcher(xdgmenu.triggers)
queue.add_application(xdgmenu)

pool.connect("watcher-changed", add_to_queue, queue)
queue.connect("processable", on_incoming_queue)

if __name__ == "__main__":
	loop = GLib.MainLoop()
	loop.run()
