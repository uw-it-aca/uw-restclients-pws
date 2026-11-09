# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Contains UW PWS DAO implementations.
"""
import os
from os.path import abspath, dirname

from restclients_core.dao import DAO


class PWS_DAO(DAO):
    def service_name(self):
        return 'pws'

    def service_mock_paths(self):
        path = [abspath(os.path.join(dirname(__file__), "resources"))]
        return path
