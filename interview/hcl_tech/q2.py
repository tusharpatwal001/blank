# decorator function for logging time

import functools, time

def timed(prefix=""):
    def deco(fn):
        @functools.wraps(fn)
        def wraper(*a, **kw):
            t = time.perf_counter()

            try:
                return fn(*a, **kw)
            finally:
                print(f"{prefix} {fn.__name__} {time.perf_counter()-t:.2f}s")

        return wraper

    return deco
