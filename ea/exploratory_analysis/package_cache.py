import os
import datetime
import json

__cache__ = {}
__cache_access__ = {}
__max_cache_len__ = 32


def clear_cache():
    global __cache__
    global __cache_access__
    __cache__ = {}
    __cache_access__ = {}


def pop_cache():
    s = sorted(__cache_access__, lambda k: (__cache_access__[k], k))
    i = s[-1]
    del __cache__[i[1]]


def cache(k, v):
    if k in __cache__:
        __cache_access__[k] = datetime.datetime.now()
    else:
        if len(__cache__) == __max_cache_len__:
            pop_cache()
        __cache__[k] = v
        __cache_access__[k] = datetime.datetime.now()


def get_index(ds, pkg):
    k = (ds.id, pkg)
    if k in __cache__:
        return __cache__[k]
    with open(os.path.join(ds.path, "%s-index.json" % pkg)) as ind:
        v = json.load(ind)
        cache(k, v)
        return v