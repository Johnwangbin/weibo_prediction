#coding:utf-8
from matplotlib import pyplot as plt
from analysis_data.fetch import *
from datetime import datetime
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import matplotlib as mpl
zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf')

'''
    to do:
    表格的显示, 多层转发个数
    文本的显示, 微博文本的显示
    
    yang xing:
    统计75分钟前的每15分钟转发深度和规模.
    根据用户关注网络,统计每一层(一般层数较小)的用户关注者的个数.
'''
class PlotTrend(object):
    def __init__(self):
        self.max_scale      = 0
        self.y_limit        = 0
        self.y_major_scale  = 0
        self.y_minor_scale  = 0
        self.trend_type     = ""

    def plot_blogger_transmission_trend(self, line):
        elements = line.strip().split(",")
        nums = map(int, elements[1:])
        try:
            blog = fetch_blog_by_id(elements[0])
            start_time  = blog.start_time
            start_minutes = start_time.hour * 60 + start_time.minute
            length = len(nums)
            plt.figure(figsize=(20,14))

            self.trend_type = "scale"
            self.plot_trend_graph(start_minutes, nums[length/2 - 1], nums[:length/2], 311)
            plt.title(u"转发规模随时间变化,开始时间:%d\n%s" % (start_minutes, blog.content),
                        fontproperties=zhfont)
            # plt.text(u"%s", blog.content)

            self.trend_type = "deep"
            self.plot_trend_graph(start_minutes, nums[length - 1], nums[length/2:], 312)
            plt.title(u"转发深度随时间变化", fontproperties=zhfont)

            self.trend_type = "rate"
            count = np.count_nonzero(nums[:length/2])
            if count == 0:
                plt.title(u"全为0,不考虑")
                raise TypeError
            zero_count = length/2-count
            nonzero_scale = nums[(length/2 - count):length/2]
            rates = np.array(nonzero_scale) / float(nonzero_scale[0]) - 1
            rates = np.array([rates[i] - rates[i-1] for i in range(1, len(rates))])
            self.plot_trend_graph(start_minutes + 15*(zero_count + 1), rates.max(), rates, 313)
            plt.title(u"转发规模增长率随时间变化", fontproperties=zhfont)

        except AttributeError:
            plt.title(u"没找到该条微博")
        except TypeError:
            plt.title(u"全为0,不考虑")

        # plt.show()


    def plot_trend_graph(self, start_minutes, max_scale, y_data, sub_plot_num):
        ax = plt.subplot(sub_plot_num)
        plt.plot([(start_minutes + 75 + i*15)/60.0 for i in range(len(y_data))],
                 y_data)
        plt.xlim(0, 96)
        self.max_scale = max_scale
        self.select_ylim()
        plt.ylim(0, self.y_limit)
        self.config_locator(ax)

    def select_ylim(self):
        y_limits = ()
        if self.trend_type == "scale":
            y_limits = (200, 500, 1000, 5000, 10000, 50000)
        elif self.trend_type == "deep":
            y_limits = (2, 5, 10, 20)
        elif self.trend_type == "rate":
            y_limits = (1, 2, 5, 10, 20, 50, 100, 1000)
        y_limit = 0
        for limit in y_limits:
            if self.max_scale < limit:
                y_limit = limit
                break
        self.y_major_scale = y_limit / 5.0
        self.y_minor_scale = y_limit / 25.0
        self.y_limit       = y_limit

    def config_locator(self, ax):
        #演示MatPlotLib中设置坐标轴主刻度标签和次刻度标签.
        #---------------------------------------------------
        xmajorLocator = MultipleLocator(24)
        xmajorFormatter = FormatStrFormatter('%d')
        xminorLocator = MultipleLocator(3)

        try:
            ymajorLocator = MultipleLocator(self.y_major_scale)
        except ValueError:
            print "11"
            pass
        ymajorFormatter = FormatStrFormatter('%.1f')
        yminorLocator = MultipleLocator(self.y_minor_scale)
        # t = arange(0.0, 100.0, 1)
        # s = sin(0.1*pi*t)*exp(-t*0.01) ax = subplot(111)
        #注意:一般都在ax中设置,不再plot中设置 plot(t,s,'--r*')
        #设置主刻度标签的位置,标签文本的格式
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.xaxis.set_major_formatter(xmajorFormatter)
        ax.yaxis.set_major_locator(ymajorLocator)
        ax.yaxis.set_major_formatter(ymajorFormatter)
        #显示次刻度标签的位置,没有标签文本
        ax.xaxis.set_minor_locator(xminorLocator)
        ax.yaxis.set_minor_locator(yminorLocator)
        ax.xaxis.grid(True, which='minor')
        #x坐标轴的网格使用主刻度
        ax.yaxis.grid(True, which='major')
        #y坐标轴的网格使用次刻度

if __name__ == "__main__":
    plot_trend = PlotTrend()
    with open("../data/trainScaleDepth.csv") as f:
        # for line in f:
        line = f.readline()
        count = 0
        for line in f:
            count += 1
            # if count < 19:
            #     continue
            if count > 50:
                break
            print count
            plot_trend.plot_blogger_transmission_trend(line)
            plt.savefig("../picture/trend_%d.jpg" % count)
