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
import sqlalchemy

from gearstore import client


def _setup_schema(dsn):
    engine = sqlalchemy.create_engine(dsn)
    conn = engine.connect()
    conn.execute('CREATE TABLE jobs (id varbinary(255) primary key, funcname'
                   ' varbinary(255), arg blob, key idx_funcname(funcname))')

class Runner(object):
    def __init__(self, client_id=None, worker_id=None, dsn=None):
        self.dsn = dsn
        self._store = sqlalchemy.Store(self.dsn)
        self.worker = gear.Worker(client_id or worker_id)

    def registerStoreFunction(self):
        self.worker.registerFunction(client.DEFAULT_STORE_FUNC)

    def run(self):
        job = self.worker.getJob()
        payload = json.loads(job.data)
        id = job.unique or uuid.uuid4()
        payload['id'] = id
        self._store.save(payload)
        job.sendWorkComplete(data=id)
