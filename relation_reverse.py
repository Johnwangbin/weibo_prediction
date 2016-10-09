from var_log import VarLog
from file_manager import FileManager
import os
from import_data import ImportData

class RelationReverse():
    def __init__(self, store_filename):
        self.filename = "weibo_dc_parse2015_link_filter"
        self.dir      = "./data/"
        self.store_dir = "./store/"
        self.relations = {}
        self.counter  = [0]
        self.store_filename = store_filename

    def line_process(self, line):
        parts       = line.split("\t")
        blogger     = parts[0]
        posterior   = parts[1]
        if posterior.strip() == "":
            return (None, None)
        return (int(blogger), [int(follower) for follower
                            in posterior.split('\x01')])

    def line_statistics(self, line):
        blogger, followers = self.line_process(line)
        if not blogger:
            return
        for follower in followers:
            if self.relations.has_key(follower):
                self.relations[follower].append(blogger)
            else:
                self.relations[follower] = []
                self.relations[follower].append(blogger)

    def name_package(self, key_or_value, times):
        parts = self.store_filename.split(".")
        return parts[0] + key_or_value + times + "." + parts[1]

    def dict_store(self, times):
        file_manager = FileManager(self.name_package("_keys_", str(times)))
        file_manager.store(self.relations.keys())
        with open(self.store_dir + self.name_package("_values_", str(times)), "w") as f:
            for value in self.relations.values():
                line = map(str, value)
                f.write(",".join(line) + "\n")

    def relation_statistics(self):
        times = 1
        self.var_log  = VarLog(self.counter)
        with open(self.dir + self.filename) as f:
            for line in f:
                if self.counter[0] < 4000000*times:
                    self.counter[0] += 1
                    self.line_statistics(line)
                else:
                    self.dict_store(times)
                    del self.relations
                    self.relations = {}
                    times += 1
            self.dict_store(times)

    #@store:"name"
    def readOneSentence(self, filename):
        counter = 0
        with open("./data/" + filename) as f:
            while 1:
                line = f.readline()
                if line == "":
                    break
                counter += 1
            print counter
        return counter

    def list_dicts(self):
        keys    = []
        values  = []
        for name in os.listdir(self.store_dir):
            if name.find("keys") != -1:
                keys.append(name)
            elif name.find("values") != -1:
                values.append(name)
        keys.sort()
        values.sort()
        return keys, values

    def import_relations(self):
        key_names, value_names = self.list_dicts()
        import_data = ImportData()
        for i in range(len(key_names)):
            with open(self.store_dir + value_names[i]) as f2:
                file_manager = FileManager(key_names[i])
                f1 = file_manager.fetch()
                import_data.batch_fill_user_and_relations3(f1, f2)

    '''
    def combine_dicts(self):
        key_names, value_names = self.list_dicts()

        value_files = []
        key_lists   = []
        for name in value_names:
            value_files.append(open(name))
        for name in key_names:
            file_manager = FileManager(name)
            key_lists.append(iter(file_manager.fetch()))
        while 1:
            for f, keys in zip(value_files, key_lists):
                line = f.readline()
                try:
                    key  = next(keys)
                except StopIteration:
                    continue
                if line != "":
                    if not self.relations.has_key(key):
                        self.relations[key] = line
                    else:
                        import_relations_data()
    '''

    def __del__(self):
        pass

if __name__ == "__main__":
    relation_reverse = RelationReverse("reverse_relation.txt")
    # relation_reverse.relation_statistics()
    relation_reverse.import_relations()