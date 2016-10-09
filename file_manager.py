import pickle

class FileManager(object):
    def __init__(self, name):
        self.path = "./store/" + name

    def store(self, data):
        with open(self.path, "wb") as f:
            pickle.dump(data, f)

    def fetch(self):
        with open(self.path, "rb") as f:
            data = pickle.load(f)
        return data

