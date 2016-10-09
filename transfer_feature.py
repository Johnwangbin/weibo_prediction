from connect_db import *


class TransferFeature(object):
    def __init__(self):
        pass

    def fetch_one_weibo(self):
        with open_session() as s:
            query = s.query(WeiboProfile)

if __name__ == "__main__":
    transfer_feature = TransferFeature()
    transfer_feature.fetch_one_weibo()


