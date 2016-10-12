#coding:utf-8
from connect_db import *
import networkx as nx

class Node:
    def __init__(self,transfer_id,reposttime):
        self._transfer_id = transfer_id
        self._reposttime = reposttime


class Graph:
    def __init__(self,graphname,graph):
        self._graphname = graphname
        self._graph = graph

G = []

def save_graph(g,weiboid):
    graph = Graph(g,weiboid)
    G.append(graph)

def readToGraph(repostdatas,blogger_id,start_time,weiboid):
    g = {}
    graph = nx.Graph(g)
    n = Node(blogger_id,start_time)
    graph.add_node(n)         #初始化图，插入父亲节点
    for result in repostdatas:
        n1 = Node(result[1],result[2]) #将节点实例化
        if (graph.has_node(n1)==False):#判断节点是否已经在图中存在
            graph.add_node(n1)#加入图
        if (result[0]==blogger_id):
            graph.add_edge(n,n1)#如果是转发的原博主微博即添加边
        else:
            for blogger_repost in repostdatas:#在转发数据里寻找n1的博主转发数据
              if(blogger_repost[1]==result[0]):
                  n2 = Node(blogger_repost[1],blogger_repost[2])
                  if (graph.has_node(n2)==False):#如果该节点不存在则实例化该节点
                      graph.add_node(n2)
                  graph.add_edge(n1,n2)#连接这两个节点
                  break

        save_graph(graph,weiboid)


def getRepostData(weiboID,blogger_id,start_time):
    with open_session() as s:
        while(len(weiboID)):
            id = weiboID.pop(0)
            results = s.query(RepostRelations.blogger_id,RepostRelations.transfer_id,RepostRelations.time_length).\
               filter(RepostRelations.weibo_id==id).all()#查询原微博的转发信息
            repostdatas =  []
            for result in results:
               repostdatas.append(list(result))#将转发信息转换为一个为二维列表




            #对原微博信息进行去重，即同一个转发者去掉转发时间更迟那项
            for repostdata1 in repostdatas:
                for repostdata2 in repostdatas:
                    if(repostdata1[1]==repostdata2[1]&repostdata1[2]>repostdata2[2]):
                        repostdatas.remove(repostdata1)



            readToGraph(repostdatas,blogger_id,start_time,id)#将转发数据和原博主读入图


def getWeiboProfileData():
    with open_session() as s:
        results = s.query(WeiboProfile)#取得所有原微博信息

        for result in results:
            getRepostData([result.id],result.blogger_id,result.start_time)#取得原微博的转发信息


if __name__ == '__main__':
    getWeiboProfileData()

