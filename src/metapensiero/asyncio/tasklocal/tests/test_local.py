# -*- coding: utf-8 -*-
# :Project:  metapensiero.asyncio.tasklocal -- Local class tests
# :Created:    lun 14 dic 2015 12:07:25 CET
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
#

import asyncio

import pytest

from metapensiero.asyncio.tasklocal import Local

def test_per_task_var(event_loop):
    mylocal = Local()

    @asyncio.coroutine
    def task_a():
        mylocal.a_var = 'foo'
        yield from asyncio.sleep(0.001) # switches to task_b
        assert mylocal.a_var == 'foo'

    @asyncio.coroutine
    def task_b():
        mylocal.a_var = 'bar'
        yield from asyncio.sleep(0.001) # switches back to task_a
        assert mylocal.a_var == 'bar'

    a = asyncio.Task(task_a(), loop=event_loop)
    b = asyncio.Task(task_b(), loop=event_loop)
    event_loop.run_until_complete(asyncio.wait((a, b), loop=event_loop))
    # check cleanup is working
    # as mylocal has been created, there will be one dict remaining
    # for when current_task() == None
    assert len(mylocal._manager.dicts) == 1

def test_local_subclass(event_loop):

    call_counter = 0

    class CustomLocal(Local):

        a_value = None

        def __init__(self, a_value):
            self.a_value = a_value
            nonlocal call_counter
            call_counter += 1

    mylocal = CustomLocal('foo')

    @asyncio.coroutine
    def task_a():
        nonlocal call_counter
        assert mylocal.a_value == 'foo'
        assert call_counter == 2
        yield from asyncio.sleep(0.001) # switches to task_b
        assert call_counter == 3

    @asyncio.coroutine
    def task_b():
        nonlocal call_counter
        assert mylocal.a_value == 'foo'
        assert call_counter == 3
        yield from asyncio.sleep(0.001) # switches back to task_a
        assert call_counter == 3

    assert call_counter == 1
    assert mylocal.a_value == 'foo'
    a = asyncio.Task(task_a(), loop=event_loop)
    b = asyncio.Task(task_b(), loop=event_loop)
    event_loop.run_until_complete(asyncio.wait((a, b), loop=event_loop))
