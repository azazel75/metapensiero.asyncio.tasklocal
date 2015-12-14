.. -*- coding: utf-8 -*-
.. :Project:   metapensiero.asyncio.tasklocal -- An asyncio's Task-local variable container
.. :Created:   dom 09 ago 2015 12:57:35 CEST
.. :Author:    Alberto Berti <alberto@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: Copyright (C) 2015 Alberto Berti
..

================================
 metapensiero.asyncio.tasklocal
================================

An asyncio's Task-local variable container
==========================================

A drop-in replacement for ``threading.local``  object that stores
per-task variables (instead of per-thread).

Really the kind of object to be tracked as "current" is configurable
by passing-in a different ``Discriminator`` instance to the ``Local``
class.

Like ``threading.local`` class, this class supports subclassing, in
which case it will rexecute the ``__init__`` method for each one of
the tracked objects.

 :author: Alberto Berti
 :contact: alberto@metapensiero.it
 :license: GNU General Public License version 3 or later

Build status
============

.. image:: https://travis-ci.org/azazel75/tasklocal.svg?branch=master
    :target: https://travis-ci.org/azazel75/tasklocal
