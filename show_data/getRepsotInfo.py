#coding:utf-8
from repost_tree import *

class getRepostInfo(object):
    def __init__(self):
        self.RepostInfo={}
        self.ans = -1

    def getRepostScale(self,TimeLength,WeiboId):
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


    def getRepostDepth(self,TimeLength,tree,WeiboId):
            self.ans = -1
            depth = self.dfs(tree._head,0,TimeLength)
            self.RepostInfo[WeiboId][int(TimeLength)/60]["depth"] = depth


    def getRostInfo(self,results):
        for result in results:
            self.RepostInfo[result.id] = {}
            buildreposttree = buildRepostTree()
            tree = buildreposttree.buildTree(result)
            for time_length in range(900,5400,900):
                self.getRepostScale(time_length,result.id)
                self.getRepostDepth(time_length,tree,result.id)
            print result.id
            print self.RepostInfo[result.id]



if __name__ == '__main__':
    getrepostinfo = getRepostInfo()
    with open_session() as s:
        results = s.query(WeiboProfile)
        getrepostinfo.getRostInfo(results)




