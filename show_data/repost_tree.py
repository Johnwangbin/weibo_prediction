#coding:utf-8
from connect_db import *

class Node:
    def __init__(self,blogger_id,transfer_id,time_length):
        self._blogger_id = blogger_id
        self._transfer_id = transfer_id
        self._time_length = time_length
        self._follower = 0
        self._children = []

    def getbloggerid(self):
        return self._blogger_id

    def gettranserid(self):
        return self._transfer_id

    def gettimelength(self):
        return self._time_length

    def getchildren(self):
        return  self._children

    def getfollowernum(self):
        return self._follower

    def add(self,node):
        self._children.append(node)

class Tree:
    def __init__(self):
        self._head = Node('header','header',0)

    def linktohead(self,node):
        self._head.add(node)


class BuildRepostTree:
    def __init__(self):
        self._tree = Tree()

    def getRepostInfo(self,weiboid):
        with open_session() as s:
            results = s.query(RepostRelations).\
                filter(RepostRelations.weibo_id == weiboid).order_by(RepostRelations.time_length).all()
        return results

    def buildTree(self,result):
        repostinfo = self.getRepostInfo(result.id)
        self._tree._head._blogger_id = result.blogger_id
        self._tree._head._transfer_id = result.blogger_id
        self._tree._head._time_length = 0
        self._tree._head._children = []
        node = []
        for repost in repostinfo:
            n = Node(repost.blogger_id,repost.transfer_id,repost.time_length)
            node.append(n)

        for n1 in node:
            for n2 in node:
                if(n1._blogger_id == self._tree._head._blogger_id):
                    if n1 not in self._tree._head._children:
                        self._tree._head.add(n1)
                        break
                if(n1._blogger_id == n2._transfer_id):
                    if n1 not in n2._children:
                        n2.add(n1)
                        break
        return self._tree







