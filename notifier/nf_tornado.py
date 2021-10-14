from . import dispatch
from . import log

import tornado.gen
import tornado.ioloop

ioloop = None

IO_READ = tornado.ioloop.IOLoop.READ
IO_WRITE = tornado.ioloop.IOLoop.WRITE
IO_EXCEPT = tornado.ioloop.IOLoop.ERROR

__timers = {}
__timer_id = 0
__dispatchers_removed = {}


def socket_add(id, method, condition=IO_READ):
    ioloop.add_handler(id, method, condition)


def socket_remove(id, condition=IO_READ):
    ioloop.remove_handler(id)


def timer_add(interval, method):
    global __timer_id

    try:
        __timer_id += 1
    except OverflowError:
        __timer_id = 0

    tid = __timer_id

    def _method(id_):
        if method():
            t = ioloop.call_later(interval / 1000.0, _method, tid)
            __timers[__timer_id] = t
        else:
            timer_remove(id_)

    t = ioloop.call_later(interval / 1000.0, _method, tid)
    __timers[__timer_id] = t

    return __timer_id


def timer_remove(id):
    """
    Removes the timer identified by the unique ID from the main loop.
    """
    t = __timers.get(id)
    if t is not None:
        t.stop()
        del __timers[id]


def dispatcher_add(method, min_timeout=True):
    @tornado.gen.coroutine
    def dispatcher(min_timeout):
        if method in __dispatchers_removed:
            __dispatchers_removed.remove(method)
            return

        while True:
            if not method():
                return
            if min_timeout:
                yield tornado.gen.sleep(dispatch.MIN_TIMER / 1000.0)
            else:
                # TODO: runs too often, should be run after each step()
                ioloop.add_callback(dispatcher), min_timeout
    ioloop.add_callback(dispatcher, min_timeout)
    return dispatch.MIN_TIMER


def dispatcher_remove(method):
    __dispatchers_removed.add(method)


def step(sleep=True, external=True):
    # FIXME: immediately exits
    ioloop.add_callback(ioloop.stop)
    ioloop.start()


def loop():
    while True:
        try:
            ioloop.start()
        except (SystemExit, KeyboardInterrupt):
            # ioloop.stop()?
            log.debug("exiting loop")
            break
        except BaseException:
            import traceback
            log.debug("exception: %s" % (traceback.format_exc(),))
            raise


def _init():
    global ioloop
    ioloop = tornado.ioloop.IOLoop.current()
