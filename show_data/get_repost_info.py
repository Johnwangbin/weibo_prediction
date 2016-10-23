#coding:utf-8
from repost_tree import *
from file_manager import  *

class GetRepostInfo(object):
    def __init__(self):
        self.RepostInfo={}
        self.ans = -1

    def getrepostscale(self, TimeLength, WeiboId):
        with open_session() as s:
            results = s.query(RepostRelations).\
                filter(RepostRelations.time_length<=TimeLength,RepostRelations.weibo_id==WeiboId).all()
        self.RepostInfo[WeiboId][int(TimeLength)/60] = {}
        self.RepostInfo[WeiboId][int(TimeLength)/60]["scale"] = len(results)+1

    def dfs(self,x,depth,TimeLength):
        if(len(x._children)==0):
            self.ans = max(self.ans,depth)
            return (self.ans)+1
        else:
            for i in range(0,len(x._children)):
                if(x._children[i]._time_length<=TimeLength):
                    self.dfs(x._children[i],depth+1,TimeLength)
                return (self.ans)+1

    def gettransfersfollower(self,weiboid):
        # if(len(x._children)==0):
        #     return
        # else:
        #     for i in range(0,len(x._children)):
        #         with open_session() as s:
        #             results = s.query(FollowerRelations.follower).\
        #                 filter(FollowerRelations.blogger == x._children[i]._transfer_id).all()
        #             if len(results) != 0:
        #                 result = str(results[0]).split(",")
        #                 if x._children[i]._transfer_id not in self.RepostInfo[weiboid]['transfers_followers'].keys():
        #                     self.RepostInfo[weiboid]['transfers_followers'][x._children[i]._transfer_id] = len(result)
        #             self.gettransfersfollower(x._children[i],weiboid)
        with open_session() as s:
            transfers = s.query(RepostRelations.transfer_id).\
                filter(RepostRelations.weibo_id == weiboid).all()
        for (transfer,) in transfers:
            with open_session() as s:
                follwer = s.query(FollowerRelations.follower).\
                    filter(FollowerRelations.blogger == transfer).all()
            if len(follwer) != 0:
                num = len(str(follwer[0]).split(","))
                if transfer not in self.RepostInfo[weiboid]['transfers_followers'].keys():
                    self.RepostInfo[weiboid]['transfers_followers'][transfer] = num

    def getrrepostdepth(self, TimeLength, tree, WeiboId):
            self.ans = 0
            depth = self.dfs(tree._head,0,TimeLength)
            self.RepostInfo[WeiboId][int(TimeLength)/60]["depth"] = depth


    def getrostinfo(self, results):
        for result in results:
            print result.id
            self.RepostInfo[result.id] = {}
            self.RepostInfo[result.id]['transfers_followers'] = {}

            with open_session() as s:
                    results = s.query(FollowerRelations.follower).\
                    filter(FollowerRelations.blogger == result.blogger_id).all()
            if(len(results)!=0):
                followers_num = len(str(results[0]).split(","))
                self.RepostInfo[result.id]['transfers_followers'][result.blogger_id] = followers_num
            self.gettransfersfollower(result.id)

            buildreposttree = BuildRepostTree()
            tree = buildreposttree.buildTree(result)

            for time_length in range(900,5400,900):
                self.getrepostscale(time_length, result.id)
                self.getrrepostdepth(time_length, tree, result.id)
            print self.RepostInfo[result.id]

if __name__ == '__main__':
    filemanager = FileManager('RepostInfo.txt')
    getrepostinfo = GetRepostInfo()
    with open_session() as s:
        results = s.query(WeiboProfile)
        getrepostinfo.getrostinfo(results)
    filemanager.store(str(getrepostinfo.RepostInfo))




