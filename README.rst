===============================
gearstore
===============================

A Gearman worker to do distributed job persistence for reliable delivery

* Free software: Apache license
* Documentation: http://docs.openstack.org/developer/gearstore
* Source: http://git.openstack.org/cgit/openstack-infra/gearstore
* Bugs: http://bugs.launchpad.net/gearstore

Inspiration
-----------

This project is inspired by dormando's Garivini. Since that one is in
Perl, and we don't like supporting perl, we are reimplementing the same
interface in python with the gear library.

See https://github.com/dormando/Garivini for more.

Features
--------

* Distributed message persistence for Gearman jobs makes persistence scale out.
* No centralized store makes system more fault tolerant.
