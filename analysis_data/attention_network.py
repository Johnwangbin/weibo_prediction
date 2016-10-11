from connect_db import *
from Queue import Queue
import bisect
from file_manager import FileManager

class AttentionNetwork(object):
    def fetch_network(self, blogger_id):
        network = []
        fetched = []
        to_fetch = [] # -1 indicates length of queue is infinite
        to_fetch.append(blogger_id)

        with open_session() as s:
            while len(to_fetch):
                id = to_fetch.pop(0)
                index = bisect.bisect_right(fetched, id) - 1
                if index == -1 or fetched[index] != id:
                    bisect.insort(fetched, id)
                    results = s.query(FollowerRelations.follower).\
                        filter(FollowerRelations.blogger==id).all()
                    followers = []
                    for result in results:
                        followers.extend(result[0].split(","))
                    to_fetch.extend(followers)
                    print id, "add:", len(followers)
                    network.append((id, followers))
                else:
                    print id, "used"
        return network

if __name__ == "__main__":
    attention_network = AttentionNetwork()
    file_manager = FileManager("attention_network")
    file_manager.store(attention_network.fetch_network(6666666))