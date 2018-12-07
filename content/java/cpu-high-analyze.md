Title: 一个应用CPU飙高的问题排查
Date: 2017-01-05 14:00
Modified: 2017-01-05 14:00
Category: java
Tags: Java,htop,jstack,jmap,cpu飙高 
Slug: cpu-high-analyze
Authors: Estel
Summary: 应用中，有些机器cpu突然飙高的排查思路

###### 问题现象
应用运行一段时间后，某些机器会cpu突然飙高，重启后会解决，但是过段时间还会发生。具体见下图：
![cpu飙高](http://img.libereco.cn/cpu-high-analyze/cpu%E9%A3%99%E9%AB%98.png)
从上述现象基本推断，代码中有bug，可能导致某些线程死循环了。
###### 排查过程
登录到发生问题的机器上，先用jstat查看gc情况，发现gc非常诡异，有大量的Full GC，且Old区空间增长非常快(jvm参数是-Xmx2g -Xms2g -Xmn512m)。见下图：
![gc情况](http://img.libereco.cn/cpu-high-analyze/gc%E6%83%85%E5%86%B5.png)
基于上述现象，推断某个线程持续不断产生了大量的对象。

为了找出出问题的线程，用htop命令，得到如下输出：
![htop情况](http://img.libereco.cn/cpu-high-analyze/htop%E6%83%85%E5%86%B5.png)
从htop的输出结果来看，线程ID为25859的线程，消耗cpu一直很高。

使用bc命令，计算25859对应的16进制数据,得到结果6503。
![bc情况](http://img.libereco.cn/cpu-high-analyze/bc%E6%83%85%E5%86%B5.png)

jstack打出当前的线程栈，找到6503的线程。
![jstack情况](http://img.libereco.cn/cpu-high-analyze/jstack%E7%BB%93%E6%9E%9C.png)
发现该线程代码，一直执行在AndroidContextUtil类的165行上。

找到该代码，如下：
![问题代码](http://img.libereco.cn/cpu-high-analyze/%E9%97%AE%E9%A2%98%E4%BB%A3%E7%A0%81.png)
至此，断定代码在此处while，有死循环。

再仔细排查分析，修复代码后，重新发布，问题解决。

###### 总结
- htop是个好工具。
- 要经常看监控，注意观察应用的指标。

###### 相关链接
- [htop](http://hisham.hm/htop/)
