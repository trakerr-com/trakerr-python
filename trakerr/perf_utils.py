import threading
import time
import psutil

# A thread-safe implementation of Singleton pattern
# To be used as mixin or base class
class PerfUtils(object):
    # use special name mangling for private class-level lock
    # we don't want a global lock for all the classes that use Singleton
    # each class should have its own lock to reduce locking contention
    __lock = threading.Lock()

    # private class instance may not necessarily need name-mangling
    _instance = None


    def __init__(self):
        """
        Do NOT call this method by initalizing this normally. Call PerfUtils.instance instead.
        """
        self._counter = _PerfCounter()
        self._counter.start()


    @classmethod
    def instance(cls):
        if not cls._instance:
            with cls.__lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    def shutdown(self):
        if self._counter is not None and self._counter.is_alive():
            self._counter.stop()

    def get_cpu_percent(self):
        return self._counter.get_cpu_percent()

    def get_mem_percent(self):
        return self._counter.get_mem_percent()

class _PerfCounter(threading.Thread):
    def __init__(self):
        super(self.__class__, self).__init__()

        #Supposedly, python doesn't do the same optimizations as other languages,
        #instance variables should be volitile.
        self._cpu_percent = 0
        self._mem_percent = 0
        self._shutdown = False
        self._lock = threading.Lock()
        psutil.cpu_percent()
        psutil.virtual_memory()

    def run(self):
        while not self._shutdown:
            time.sleep(1)
            mem = psutil.virtual_memory()
            with self._lock:
                self._cpu_percent = psutil.cpu_percent()
                self._mem_percent = mem.percent

    def stop(self):
        self._shutdown = True

    def get_cpu_percent(self):
        with self._lock:
            return self._cpu_percent

    def get_mem_percent(self):
        with self._lock:
            return self._mem_percent
