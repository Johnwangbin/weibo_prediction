import time
from threading import Timer


class VarLog(object):
    def __init__(self, var_ref):
        self.var_ref = var_ref
        self.initial_logging_timer()

    def func(self):
        while 1:
            print("%d %s" % (self.var_ref[0], time.strftime("%I:%M:%S")))
            time.sleep(10)

    def initial_logging_timer(self):
        self.timer = Timer(1, self.func)
        self.timer.start()