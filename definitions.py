from file_manager import FileManager


class Feature(object):
    def __init__(self):
        self.fileManager = FileManager(self.__str__())

    def store(self):
        pass

    def fetch(self):
        pass

    def __getitem__(self, item):
        pass

    def __str__(self):
        pass

class Output(object):
    def fetch(self):
        pass

    def __getitem__(self, item):
        pass

class Blogs(object):
    def __init__(self):
        emotion_polars  = 0
        topic_heats     = 0
        blogger_attentions = 0

        spread_scale = 0
        spread_deep  = 0
