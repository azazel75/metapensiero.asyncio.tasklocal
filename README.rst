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

 :author: Alberto Berti
 :contact: alberto@metapensiero.it
 :license: GNU General Public License version 3 or later
