# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_gearstore
----------------------------------

Tests for `gearstore.runner` module.
"""

import time

import gear
import fixtures

from gearstore import client
from gearstore import runner
from gearstore.store import sqlalchemy as store  # XXX: can haz plugins?
from gearstore.tests import base


class TestGearstoreWorker(base.TestCase):
    def setUp(self):
        super(TestGearstoreWorker, self).setUp()
        self.server = gear.Server(port=0)

    def test_runner(self):
        c = client.Client()
        c.addServer('127.0.0.1', port=self.server.port)
        sqlite_dir = self.useFixture(fixtures.TempDir()).path
        dsn = 'sqlite://%s/jobs.sqlite' % sqlite_dir
        store.Store(dsn).initialize()
        r = runner.Runner(client_id='test_runner', dsn=dsn)
        r.addServer('127.0.0.1', port=self.server.port)
        c.waitForServer()
        r.waitForServer()
        r.registerStoreFunction()
        j = c.submitJob('test_store_job', 'payload')
        r.run()
        self.assertIsNone(j.failure)
        self.assertTrue(j.complete)
        # Job should be stored now, but not sent to a worker just yet. Test
        # this happened by shutting down gearman server and starting a new one.
        self.server.shutdown()
        self.server = gear.Server(port=0)
        r.waitForServer()
        real_worker = gear.Worker(worker_id='real_worker')
        real_worker.addServer('127.0.0.1', port=self.server.port)
        real_worker.registerFunction('test_store_job')
        j = real_worker.getJob()
        self.assertEqual('test_store_job', j.name)
        self.assertEqual('payload', j.data)
