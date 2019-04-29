Title:一个高并发性能压测的实例
Date: 2016-12-01 14:00
Modified: 2016-12-01 14:00
Category: Technology
Tags: 高并发,Jmeter,压测,DNS负载均衡,LVS,长连接,Https
Slug: jmeter-pressure-test
Authors: Estel
Summary: 压测性能不好，未必是应用本身性能不好。很有可能压测系统本身有性能瓶颈或者网络有瓶颈。压测是个系统工程，需要把握系统的整个链路，才能压出系统应有的指标。

#### 背景
本人所在的公司提供的是Sass公有云风控服务。某国内Top5的电商公司，想接入公有云服务，需要做个压测。

压测要求：

- 并发36000(此处的理解有歧义，应该想表达的是qps 36000)。
- 响应时间200ms以内。

压测准备：

- 扩容(根据之前的系统性能数据)
	- 扩容java web服务器
	- 扩容memcached
- 运维
   - 扩容带宽(Ucloud带宽)
   - Nginx取消对单IP的10000 TPS限制
- 脚本
   - 该电商准备压测脚本 

参与人员：

- 我方
	- 开发工程师小明(驻地：杭州)
- 对方
	- 测试工程师小红(驻地：上海)

#### Jmter瓶颈
小红把单机Jmeter脚本跑起来，线程数不断往上增加。结果发现，增加到3000左右TPS的时候，性能怎么都上不去了，甚至开始大量报错。错误如下：

```java
Too many open files. Stacktrace follows:
java.net.SocketException: Too many open files
    at java.net.Socket.createImpl(Socket.java:397)
    at java.net.Socket.getImpl(Socket.java:460)
    at java.net.Socket.setSoTimeout(Socket.java:1017)
    at org.apache.http.conn.scheme.PlainSocketFactory.connectSocket(PlainSocketFactory.java:126)
    at org.apache.http.impl.conn.DefaultClientConnectionOperator.openConnection(DefaultClientConnectionOperator.java:180)
    at org.apache.http.impl.conn.ManagedClientConnectionImpl.open(ManagedClientConnectionImpl.java:294)
    at org.apache.http.impl.client.DefaultRequestDirector.tryConnect(DefaultRequestDirector.java:640)
    at org.apache.http.impl.client.DefaultRequestDirector.execute(DefaultRequestDirector.java:479)
    at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:906)
    at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:805)
    at groovyx.net.http.HTTPBuilder.doRequest(HTTPBuilder.java:476)
    at groovyx.net.http.HTTPBuilder.doRequest(HTTPBuilder.java:441)
    at groovyx.net.http.HTTPBuilder.request(HTTPBuilder.java:390)
```
小红看到这个错误，第一反应是服务端挂挂了。 于是微信通知小明，你们性能不行，服务在不停抛异常，已经挂了。小明马上去线上排查日志，结果发现Nginx毫无压力，Java程序也运行正常，毫无压力。双方争执了半天。 

后经过分析，才发现，Nginx不可能抛出这个异常，Nginx最多报个500的错误，这异常不是后端返回的，是Jmeter自己抛出的。单机Jmeter不断创建连接，导致文件描述符不够用了。

查看linux设置，ulimit -a，发现大小以及设置为65536。那么问题来了，同一个请求，这么多都不够用的呢 ？

原来，Nginx设置了，只支持短连接。(这是业务决定的，业务场景里，基本都是1次请求居多)

临时调整Nginx配置，支持长连接。继续压测，调高线程数，结果发现，到了5000左右TPS，再也上不去了，服务端开始出现大量超时。

#### 负载均衡瓶颈
小明仔细观察监控，发现java应用的响应时间，压根没啥变化，表现非常好。于是把怀疑对象放在网络上，一边问运维，带宽是不是不够用了；一边和对方小红扯，单机网络有瓶颈，能不能用集群压测。结果，运维说，300M入口带宽，才用了一点；小红说单机网卡是百兆的，出口带宽也很高；

僵持不下，小明又去线上看监控，想看看Nginx日志里，能不能有新发现。结果。。。 无意中发现，小红压测的所有的请求，都落在了一台Nginx机器上。这是为啥，负载不均衡 ？？？

找到运维沟通，才发现，集群是用DNS负载均衡的！网络架构如下图：
![DNS负载均衡](http://img.libereco.cn/performance/DNS%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1.png)

由于压测时在单机进行的，而单机有DNS缓存，所以总是访问同一台机器。

#### Load Balance 调优
如何单机压测做到负载均衡呢？想到了Load Balance，可以基于TCP/IP层做负载均衡。于是对网络做改造，改造后的架构如下：
![Load Balance负载均衡](http://img.libereco.cn/performance/LoadBalance%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1.png)

调整后，继续压测，发现，所有请求还是全部都落到了一台机器上。看配置参数，发现默认IP保持了，即同一个IP，所有请求，会保持往同一台机器做负载均衡。

调整为随机分发后，终于负载均衡了。

单机运行Jmeter压测到17000 TPS后，就再也上不去了。服务端Nginx和Java程序均运行平稳，性能无变化。 基本可以断定，是单机Jmeter到了瓶颈。

#### 后记
**压测完成后，忘记把Nginx单机10000 TPS的限制去掉，结果，有一天突然有个合作方，未通知我们就做压测，差点把整个集群压挂！!**

#### 总结
- 压测机器，条件允许的话，最好单独搭建。
- 限流服务应该提供基于白名单的限流机制。
- Jmeter单机压测瓶颈很大。
- 当压测方不是分布式集群的时候，负载均衡方式对压测结果影响非常大。
- 跨公网的压测，成本高，效果也未必好，受公网环境影响大。

#### 相关连接
- [Jmeter](http://jmeter.apache.org/)
- [全链路压测](http://open.taobao.com/doc2/detail.htm?articleId=103188&docType=1&treeId=2)
- [LVS](http://zh.linuxvirtualserver.org/)
- [Ucloud Load Balancer](https://www.ucloud.cn/site/product/ulb.html)
- [一分钟了解负载均衡的一切](http://mp.weixin.qq.com/s?src=3&timestamp=1481702253&ver=1&signature=xqjBIqXRrTSrhO9bVfPMKw*Gg90a6ZTGaG2SA1uH4jNUkPvbrhD5PmM8Y6dZj3aYwZHHf2S*leeSBgCGPxEvI3xxHAy9bDt7cG9YkLo6qPbBM3Z9dfJCm7ypIaGZZc9zLiJmlG1aSg5sJ1AJD6wU7DNDB88d8XWcWh24w2xs8dk=)
