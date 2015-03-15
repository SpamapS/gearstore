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

import argparse
import logging
import socket

from gearstore import stocker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('servers', nargs='+', help='Servers to connect to, '
                        ' format of host/port')
    parser.add_argument('--sqlalchemy-dsn', help='SQLAlchemy DSN to store in')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    stkr = stocker.Stocker(
        client_id=socket.gethostname(), dsn=args.sqlalchemy_dsn)
    for s in args.servers:
        if '/' in s:
            (host, port) = s.split('/', 2)
            stkr.addServer(host, port)
        else:
            stkr.addServer(s)

    stkr.waitForServer()
    while True:
        stkr.stock()
        stkr.ship()
