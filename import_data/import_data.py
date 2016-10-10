#coding:utf-8
from connect_db import *
from var_log import VarLog
import logging
from relations_iter import RelationsIterFactory
from traceback import print_exc
from itertools import izip
from datetime import datetime

class BatchCollectAndCommit(object):
    def __init__(self, counter):
        self.count = 0
        self.counter = counter

    def __call__(self, lines, session, table):
        self.counter[0] += 1
        if self.count < 10000:
            self.count += 1
        else:
            session.execute(
                table.__table__.insert(),
                lines
            )
            self.count = 0
            session.commit()
            lines[:] = []

class ImportData(object):
    def __init__(self):
        self.initial_filenames()
        self.counter = [0]
        self.var_log = VarLog(self.counter)
        # self.mappering_tables()

    def initial_filenames(self):
        self.relations_filename = "weibo_dc_parse2015_link_filter"
        self.weibo_filename  = "WeiboProfile.train"
        self.transmit_relations_filename = "trainRepost.txt"

    def mappering_tables(self):
        relations_table = Table("relations", metadata, autoload=True)
        mapper(Relations, relations_table)

    def fill_user_and_relations(self):
        session = sessionmaker(engine)()
        with open("./data/"+ self.relations_filename) as f:
            line = f.readline().strip()
            blogger     = int(line.split("\t")[0])
            posterior   = line.split('\t')[1]
            for follower in posterior.strip().split('\x01'):
                try:
                    r = Relations()
                    r.blogger = blogger
                    r.follower = int(follower)
                    session.add(r)
                except:
                    print follower
            session.flush()
        session.commit()

    def relations_process(self, iter):
        for line in iter:
            parts       = line.split("\t")
            blogger     = parts[0]
            posterior   = parts[1]
            if posterior.strip() == "":
                continue
            self.counter[0] += 1
            for follower in posterior.split('\x01'):
                yield {"blogger":int(blogger), "follower":int(follower)}

    def batch_fill_user_and_relations(self):
        session = sessionmaker(engine)()
        relations_iter_factory = RelationsIterFactory(self.relations_filename)
        try:
            while not relations_iter_factory.is_end:
                relations_iter = relations_iter_factory.create_iter()
                session.execute(
                    Relations.__table__.insert(),
                    [relation for relation in self.relations_process(relations_iter)]
                )
                session.commit()
        except:
            print_exc()

    def relations_line_process(self, line):
        parts       = line.split("\t")
        blogger     = parts[0]
        posterior   = parts[1]
        if posterior.strip() == "":
            return []
        self.counter[0] += 1
        return [{"blogger":int(blogger), "follower":int(follower)}
                for follower in posterior.split('\x01')]

    def batch_fill_user_and_relations2(self):
        session = sessionmaker(engine)()
        with open("./data/" + self.relations_filename) as f:
            count = 0; lines = []
            for line in f:
                if count < 10000:
                    count += 1
                else:
                    session.execute(
                        Relations.__table__.insert(),
                        lines
                    )
                    session.commit()
                    count = 0
                    lines = []
                lines.extend(self.relations_line_process(line))

    def cut_string_to_parts(self, line):
        length  = 50
        count   = 0
        lines   = []
        followers = line.split(",")
        while count*length < len(followers):
            lines.append(",".join(followers[count*length:(count+1)*length]))
            count += 1
        return lines

    def transfer_relation_process(self, line):
        parts = line.split('\x01')
        return {"weibo_id": parts[0], "blogger_id": int(parts[1]), "transfer_id":
                int(parts[2]), "time_length": int(parts[3]),
                "content":parts[4].strip().decode("utf-8")}

    def weibo_profile_process(self, line):
        parts = line.split("\x01")

        return {"id": parts[0], "blogger_id": int(parts[1]), "start_time":
                datetime.strptime(parts[2], "%H:%M:%S"), "content":parts[3].strip()}

    def batch_fill_user_and_relations3(self, f1, f2):
        with open_session() as s:
            batch_manager = BatchCollectAndCommit(self.counter)
            lines = []
            for key, value in izip(f1, f2):
                batch_manager(lines, s, FollowerRelations)
                lines.extend([{"blogger":key, "follower":followers}
                    for followers in self.cut_string_to_parts(value.strip())])

            s.execute(
                FollowerRelations.__table__.insert(),
                lines
            )
            s.commit()

    def batch_fill_transfer_relations_table(self):
        with open("./data/trainRepost.txt") as f, open_session() as s:
            batch_manager = BatchCollectAndCommit(self.counter)
            lines = []
            for line in f:
                batch_manager(lines, s, RepostRelations)
                lines.append(self.transfer_relation_process(line))

            # when the num is not come to 10000, just commit
            s.execute(
                RepostRelations.__table__.insert(),
                lines
            )
            s.commit()

    def batch_fill_weibo_profile_table(self):
        with open("./data/WeiboProfile.train") as f, open_session() as s:
            batch_manager = BatchCollectAndCommit(self.counter)
            lines = []
            for line in f:
                batch_manager(lines, s, WeiboProfile)
                lines.append(self.weibo_profile_process(line))

            # when the num is not come to 10000, just commit
            s.execute(
                WeiboProfile.__table__.insert(),
                lines
            )
            s.commit()

    def readOneSentence(self, filename):
        counter = 0
        with open("./data/" + filename) as f:
            while 1:
                line = f.readline()
                if line == "":
                    break
                counter += 1
            print counter

if __name__ == "__main__":
    import_data = ImportData()
    # import_data.batch_fill_transfer_relations_table()
    # import_data.batch_fill_user_and_relations2()
    # import_data.batch_fill_weibo_profile_table()
    # import_data.readOneSentence("WeiboProfile.train")
    # import_data.readOneSentence("trainRepost.txt")
    # import_data.fill_user_and_relations()