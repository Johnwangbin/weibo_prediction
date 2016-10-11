python为2.7版本。安装pycharm, git. 在pycharm VCS标签下,选择check from version control,选择git.
在新的对话框中输入git地址为https://github.com/Johnwangbin/weibo_prediction.git 即可clone下竞赛的代码。

当一个功能写好后，通过VCS标签下的，commit changes, 即可将修改提交到github服务器。注意过程中要选择commit and push.

1.存储
每条微博对应一个样本;
输入：用户间关注关系网络。
输出：用户间转发关系树（同一微博不可能被相同用户多次转发）。
使用数据结构或者第三方库，将上述两个结构存储于内存当中,当然要能很轻松得到图和树的所有特征，转发树要有时间属性。陈老师之前好像有发过。

2.分析
（1）画出输入和输出的图形，对比他们的特征。
（2）编写效果评定程序，选择模型，将样本用于训练，调节参数。

3.效果评定
 预测值和真实值比较。评定方法见竞赛网站评分标准处。

