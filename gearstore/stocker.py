# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import uuid

import gear

from gearstore import client
from gearstore.store import sqla


class Stocker(object):
    def __init__(self, client_id=None, worker_id=None, dsn=None):
        self.dsn = dsn
        self._store = sqla.Store(self.dsn)
        self.worker = gear.Worker(client_id or worker_id)
        client_id_client = '%s_shipper' % (client_id or worker_id)
        self.client = gear.Client(client_id_client)

    def addServer(self, *args, **kwargs):
        self.worker.addServer(*args, **kwargs)
        self.client.addServer(*args, **kwargs)

    def waitForServer(self):
        self.worker.waitForServer()
        self.client.waitForServer()

    def registerStoreFunction(self):
        self.worker.registerFunction(client.DEFAULT_STORE_FUNC)

    def stock(self):
        job = self.worker.getJob()
        payload = json.loads(job.arguments)
        unique = job.unique or bytes(uuid.uuid4())
        payload['unique'] = unique
        self._store.save(payload)
        job.sendWorkComplete(data=unique)

    def ship(self):
        for job in self._store.consume():
            gjob = gear.Job(job['funcname'], job['arg'], job['unique'])
            self.client.submitJob(gjob)
