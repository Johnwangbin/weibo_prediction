from connect_db import *

class ImportOneData():
    def __init__(self):
        session = sessionmaker(engine)()

    def import_one_relation(self, blogger, follower):
        relation = Relations()
        # relation.blogger =