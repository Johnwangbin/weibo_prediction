__author__ = 'liying'
'''
    def batch_fill_user_and_relations(self):
        session = sessionmaker(self.engine)()
        with open("./data/"+ self.relations_filename) as f:
            lines = (line for line in f)
            while self.count < 30000:
                self.count += 1
                lines = (self.counter(line) for line in lines if self.count % 10000 != 0)

                def split_lines(line):
                    parts = line.split("\t")
                    return parts

                parts     = (split_lines(line) for line in lines)
                couples   = ((blogger, f) for (blogger, posterior) in parts
                             for f in posterior.strip().split('\x01'))
                session.execute(
                    Relations.__table__.insert(),
                    [{"blogger":int(blogger), "follower":int(follower)}
                     for blogger, follower in couples if follower]
                )
                session.flush()
            session.commit()
'''
import binascii
import chardet

from file_manager import FileManager


def test():
    a = [0,0]
    b = [1,2]
    file_manager = FileManager("test.txt")
    file_manager.store(a)
    file_manager.store(b)

def o(line):
    line[:] = []

def transfer_relation_process(line):
        parts = line.split('\x01')
        return {"weibo_id": parts[0], "blogger_id": int(parts[1]), "transfer_id":
                int(parts[2]), "time_length": int(parts[3]), "content":parts[4]}

def weibo_process(b_text):
    i = 0
    a_text = ""
    pos = 0;last_pos = 0
    while pos != -1:
        last_pos = pos
        pos = b_text.find("\xF8", pos)
        if pos != -1:
            a_text += b_text[last_pos:pos]
            pos += 4
        else:
            a_text += b_text[last_pos:]
    return a_text

if __name__ == "__main__":
    with open("./data/trainScaleDepth.csv") as f:
        txt = f.readline()
        print txt
        print f.readline()
    '''
    part = txt.split("\x01")[3].strip()
    print part
    print [part]
    print int(part[0],16) & 0xf8
    print weibo_process(part)
    '''

    # print transfer_relation_process(txt.split("\n")[0])
    # line = [1,2,3]
    # o(line)
    # print line
    # file_manager = FileManager("reverse_relation_keys_1.txt")
    # list = file_manager.fetch()[:500]
    # print list
    # test()
    # a = {1:"a", 2:"b", 3:"c"}
    # b = map(str, a.keys())