# -*- coding: utf-8 -*-

"""Unittests for Janitoo-Roomba Server.
"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time, datetime
import unittest
import threading
import logging
from pkg_resources import iter_entry_points

from janitoo_nosetests.server import JNTTServer, JNTTServerCommon
from janitoo_nosetests.thread import JNTTThread, JNTTThreadCommon
from janitoo_nosetests.thread import JNTTThreadRun, JNTTThreadRunCommon
from janitoo_nosetests.component import JNTTComponent, JNTTComponentCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

from janitoo_raspberry_i2c_bmp.bmp import BMPComponent

class TestBMPComponent(JNTTComponent, JNTTComponentCommon):
    """Test the component
    """
    component_name = "rpii2c.bmp"

class TestBMPThread(JNTTThreadRun, JNTTThreadRunCommon):
    """Test the datarrd thread
    """
    thread_name = "rpii2c"
    conf_file = "tests/data/janitoo_raspberry_i2c_bmp.conf"

    def test_101_check_values(self):
        self.skipRasperryTest()
        self.wait_for_nodeman()
        time.sleep(5)
        self.assertValueOnBus('bmp1','temperature')
        self.assertValueOnBus('bmp1','altitude')
        self.assertValueOnBus('bmp1','pressure')
        self.assertValueOnBus('bmp1','sealevel_pressure')

    def test_102_get_values(self):
        self.onlyRasperryTest()
        self.wait_for_nodeman()
        time.sleep(5)
        temperature = self.thread.bus.nodeman.find_value('bmp1','temperature').data
        print(temperature)
        altitude = self.thread.bus.nodeman.find_value('bmp1','altitude').data
        print(altitude)
        pressure = self.thread.bus.nodeman.find_value('bmp1','pressure').data
        print(pressure)
        sealevel_pressure = self.thread.bus.nodeman.find_value('bmp1','sealevel_pressure').data
        print(sealevel_pressure)
        self.assertNotEqual(temperature, None)
        self.assertNotEqual(altitude, None)
        self.assertNotEqual(pressure, None)
        self.assertNotEqual(sealevel_pressure, None)
        self.assertNotInLogfile('^ERROR ')
