# -*- coding: utf-8 -*-
# :Project:  metapensiero.asyncio.tasklocal -- Discriminator tests
# :Created:    dom 13 dic 2015 23:15:17 CET
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
#

import asyncio

import pytest

from metapensiero.asyncio.tasklocal import TaskDiscriminator

def test_current(event_loop):

    disc = TaskDiscriminator(loop=event_loop)

    async def task_a():
        ctask = asyncio.Task.current_task(loop=event_loop)
        assert ctask is a
        assert disc.current() is ctask
        await asyncio.sleep(0.001) # this will force a switch to the
        # other task
        assert disc.current() is ctask

    async def task_b():
        ctask = asyncio.Task.current_task(loop=event_loop)
        assert ctask is b
        assert disc.current() is ctask
        await asyncio.sleep(0.001)
        assert disc.current() is ctask

    a = asyncio.Task(task_a(), loop=event_loop)
    b = asyncio.Task(task_b(), loop=event_loop)
    assert a is not b
    event_loop.run_until_complete(asyncio.wait((a, b), loop=event_loop))


def test_dispose(event_loop):

    disc = TaskDiscriminator(loop=event_loop)

    a_completed = False
    b_completed = False

    def a_dispose_handler(_):
        nonlocal a_completed
        a_completed = True

    def b_dispose_handler(_):
        nonlocal b_completed
        b_completed = True

    async def task_a():
        disc.dispose(a_dispose_handler)

    async def task_b():
        disc.dispose(b_dispose_handler)

    a = asyncio.Task(task_a(), loop=event_loop)
    b = asyncio.Task(task_b(), loop=event_loop)
    event_loop.run_until_complete(asyncio.wait((a, b), loop=event_loop))
    assert a_completed is True
    assert b_completed is True
