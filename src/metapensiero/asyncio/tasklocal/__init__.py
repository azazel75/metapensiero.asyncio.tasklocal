# -*- coding: utf-8 -*-
# :Project:   metapensiero.asyncio.tasklocal -- An asyncio's Task-local variable container
# :Created:   dom 09 ago 2015 12:57:35 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015 Alberto Berti
#

import asyncio
import weakref
import functools

__all__ = ('BaseDiscriminator', 'TaskDiscriminator', 'Local')


class BaseDiscriminator:
    """The base class for an object devoted to manage a generic set of
    omogenous objects where only one is 'elected' current at a certain
    point in time.
    """

    def current(self):
        """Get the current object"""
        raise NotImplementedError

    def dispose(self, handler):
        """Associate an handler to be called when the object ends its purpose
        or gets finalized.
        """
        obj = self.current()
        if obj:
            weakref.ref(obj, handler)


class TaskDiscriminator(BaseDiscriminator):
    """A specialized discriminator that knows how to deal with tasks"""

    __slots__ = ('loop',)

    def __init__(self, loop=None):
        self.loop = loop

    def current(self):
        return asyncio.Task.current_task(self.loop)

    def dispose(self, handler):
        """The handler gets called when th task completes rather than when it
        is destructed.
        """
        task = self.current()
        if task:
            task.add_done_callback(handler)


class DictManager:
    """A class that manages per-object dict, using the provided
    'discriminator' object or the default that is capable of handling tasks.

    The object returned by discriminator.current() must be hashable.
    """
    __slots__ = ('dicts', 'discriminator')

    def __init__(self, *, discriminator=None):
        self.discriminator = discriminator or TaskDiscriminator()
        self.dicts = {}

    def get_dict(self):
        """Return the dict for the current object  or  raises a KeyError.
        """
        obj_id = hash(self.discriminator.current())
        return self.dicts[obj_id][1]

    def create_dict(self):
        obj_id = hash(self.discriminator.current())
        handler = functools.partial(self._cleanup_dict, obj_id)
        # have to better deal with references?
        self.discriminator.dispose(handler)
        localdict = {}
        # save a ref to the handler in the case the discriminator
        # handles it the weak way
        self.dicts[obj_id] = (handler, localdict)
        return localdict


    def _cleanup_dict(self, obj_id, _):
        if obj_id in self.dicts:
            del self.dicts[obj_id]


class Local:
    """A more generic drop-in replacement for threading.local.

    It doesn't setup any lock so it cannot be considered thread-safe.
    """
    __slots__ = ('_localargs', '_manager', '__dict__')

    def __new__(cls, *args, discriminator=None, **kwargs):
        if (args or kwargs) and (cls.__init__ is object.__init__):
            raise TypeError("Initialization arguments are not supported")
        self = object.__new__(cls)
        manager = DictManager(discriminator=discriminator)
        object.__setattr__(self, '_manager', manager)
        object.__setattr__(self, '_localargs', (args, kwargs))
        manager.create_dict()
        return self

    def _setup_dict(self):
        manager = object.__getattribute__(self, '_manager')
        try:
            map = manager.get_dict()
        except KeyError:
            map = manager.create_dict()
            args, kwargs = object.__getattribute__(self, '_localargs')
            object.__getattribute__(self, '__init__')(*args, **kwargs)
        object.__setattr__(self, '__dict__', map)

    def __getattribute__(self, name):
        object.__getattribute__(self, '_setup_dict')()
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name == '__dict__':
            raise AttributeError(
                "%r object attribute '__dict__' is read-only"
                % self.__class__.__name__)
        object.__getattribute__(self, '_setup_dict')()
        return object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name == '__dict__':
            raise AttributeError(
                "%r object attribute '__dict__' is read-only"
                % self.__class__.__name__)
        object.__getattribute__(self, '_setup_dict')()
        return object.__delattr__(self, name)
