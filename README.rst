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

 :author: Alberto Berti
 :contact: alberto@metapensiero.it
 :license: GNU General Public License version 3 or later

An asyncio's Task-local variable container
==========================================

Usage
+++++

A drop-in replacement for ``threading.local``  object that stores
per-task variables (instead of per-thread). You can use it like this::

  import asyncio
  from metapensiero.asyncio.tasklocal import Local

  mylocal = Local()

  @asyncio.coroutine
  def task_a():
      mylocal.a_var = 'foo'
      yield from asyncio.sleep(0.001) # switches to task_b
      assert mylocal.a_var == 'foo'
      print(mylocal.a_var)

  @asyncio.coroutine
  def task_b():
      mylocal.a_var = 'bar'
      yield from asyncio.sleep(0.001) # switches back to task_a
      assert mylocal.a_var == 'bar'
      print(mylocal.a_var)

  loop = asyncio.get_event_loop()
  a = asyncio.Task(task_a())
  b = asyncio.Task(task_b())
  loop.run_until_complete(asyncio.wait((a, b)))

  # this prints out:
  # foo
  # bar

Really the kind of object to be tracked as "current" is configurable
by passing-in a different ``Discriminator`` instance to the ``Local``
class.

By default it will use the ``TaskDiscriminator`` supplied with the
package. It will use standard ``asyncio``'s loop detection techniques
(by delegating it to ``asyncio.Task.current_task()``) but if you want
to track tasks of a particular event loop, you can supply your own
``TaskDiscriminator`` instance to the ``Local`` instance
initialization, like this::

  from metapensiero.asyncio.tasklocal import Local, TaskDiscriminator

  mylocal = Local(discriminator=TaskDiscriminator(loop=my_loop))

You can also track another set of object by subclassing the
``BaseDiscriminator`` class::

  from metapensiero.asyncio.tasklocal import BaseDiscriminator

  class ASampleSessionDiscriminator(BaseDiscriminator):

      def current(self):
          return current_session()

  mylocal = Local(discriminator=ASampleDiscriminator())

You have to implement at least the ``current`` method.

Like ``threading.local`` class, this class supports subclassing, in
which case it will re-execute the ``__init__`` method for each one of
the tracked objects::

  call_counter = 0

  class CustomLocal(Local):

      a_value = None

      def __init__(self, a_value):
          self.a_value = a_value
          nonlocal call_counter
          call_counter += 1

  mylocal = CustomLocal('foo')

Here ``mylocal.a_value`` will be initialized to ``foo`` for every
tracked object (asyncio's tasks by default). Here ``call_counter``
will count the number of every tracked object in which the ``mylocal``
object has been accessed.

Testing
+++++++

To run the tests you should run the following at the package root::

  python setup.py test

Build status
++++++++++++

.. image:: https://travis-ci.org/azazel75/tasklocal.svg?branch=master
    :target: https://travis-ci.org/azazel75/tasklocal
