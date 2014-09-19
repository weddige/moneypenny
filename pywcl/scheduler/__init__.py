# -*- coding: UTF-8 -*-
from datetime import datetime
from threading import Timer
from queue import Queue
import uuid
import logging
#Fallbacl for python < 3.3
try:
    from time import perf_counter
except ImportError:
    from time import clock as perf_counter

log = logging.getLogger(__name__)

class _Task:
    _processing_time = 10
    _scheduler = None
    def __init__(self, function, due=None, interval=None, repeat=0):
        self._function = function
        if hasattr(due, '__iter__'):
            self._due_iter = iter(due)
            self._due = self._due_iter.__next__()
        else:
            self._due_iter = None
            self._due = due
        self._interval = interval
        self._repeat = repeat
        if not (self._due or self._interval):
            raise ValueError

    def __call__(self, *args, job_uuid=None, **kwargs):
        start = perf_counter()
        result = self._function(*args, **kwargs)
        self._processing_time = perf_counter() - start
        if self._scheduler:
            del self._scheduler._scheduled[job_uuid]
            if self._interval and self._repeat != 1:
                if self._repeat > 0:
                    self._repeat -= 1
                self._scheduler.schedule(self, *args, job_uuid=job_uuid, **kwargs)
            if self._due_iter:
                self._due = self._due_iter.__next__()
                if self._due:
                    self._scheduler.schedule(self, *args, job_uuid=job_uuid, **kwargs)
        return result

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        new_func = self._function.__get__(obj, type)
        return self.__class__(new_func, self._due_iter or self._due, self._interval, self._repeat)

class Task:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, function):
        return _Task(function, *self.args, **self.kwargs)

class Scheduler:
    _queue = Queue()
    _scheduled = dict()

    def __init__(self):
        pass

    def schedule(self, function, *args, job_uuid=None, **kwargs):
        if isinstance(function, _Task):
            if not job_uuid:
                job_uuid = uuid.uuid4() 
            kwargs['job_uuid'] = job_uuid  
            function._scheduler = self
            if function._interval:
                timer = Timer(function._interval, function, args, kwargs)
            else:
                remainder = (function._due - datetime.now()).total_seconds()
                timer = Timer(remainder - function._processing_time, function, args, kwargs)       
            self._scheduled[job_uuid] = timer
            timer.start()
            return job_uuid
        else:
            self.queue.put((function, args, kwargs))

    def cancel(self, job_uuid=None):
        if job_uuid:
            self._scheduled[job_uuid].cancel()
            del self._scheduled[job_uuid]
        else:
            for job_uuid in self._scheduled:
                self._scheduled[job_uuid].cancel()
                del self._scheduled[job_uuid]
