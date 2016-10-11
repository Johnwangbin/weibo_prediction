from var_log import VarLog

'''
class RelationsIter(object):
    def __init__(self, filename):
        self.filename = filename
        self.counter_container = [0]
        self.last_counter = -1
        self.var_log = VarLog(self.counter_container)
        self.f = open("./data/"+ self.filename)

    def __iter__(self):
        for line in self.f:
            if self.counter_container[0] >=5000:
                raise StopIteration()
            self.counter_container[0] += 1
            parts = line.strip().split("\t")
            try:
                followers = parts[1].split("\x01")
            except IndexError:
                continue
            blogger = parts[0]
            for follower in followers:
                try:
                    yield {"blogger":int(blogger), "follower":int(follower)}
                except:
                    continue

    def is_end(self):
        if self.last_counter == self.counter_container[0]:
            return True
        self.last_counter = self.counter_container[0]
        return False
'''

class RelationsIterFactory():
    def __init__(self, filename):
        self.pos = 0
        self.f   = open("./data/" + filename)
        self.is_end = False
    '''
    def create_iter(self):
        self.f.seek(self.pos)
        for i in xrange(10000):
            line = self.f.readline()
            if line == "":
                self.is_end = True
                return
            yield line
        self.pos = self.f.tell()
    '''

    def __del__(self):
        self.f.close()


