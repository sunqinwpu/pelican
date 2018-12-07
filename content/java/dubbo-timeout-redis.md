Title: Dubbo服务周期性超时问题排查
Date: 2016-08-05 14:00
Modified: 2016-08-05 14:00
Category: java
Tags: Java,Dubbo,Timeout,Redis,刷盘 
Slug: dubbo-timeout-redis
Authors: Estel
Summary: Dubbo服务周期性超时问题排查思路，最终定位为Redis周期性刷盘导致。排查过程值得思考

##### 问题背景
新公司刚入职、接手的系统有个奇怪的现象，A系统通过Dubbo服务调用B系统的几个服务，每隔十几分钟均出现大量的超时。对这种问题，也算是见多识广，不过这次排查也着实耗费了不少精力，走了不少弯路。

发生问题的日志如下：

![fp-titan-architecture](http://img.libereco.cn/fp-dubbo-exception-1.png "A系统异常1")
##### 整体架构
- 整体架构

![fp-titan-architecture](http://img.libereco.cn/fp-titan-architecture.png "系统整体架构")

- 整体负载
	- A集群Web请求TPS 8000左右
	- B集群Web请求TPS 800左右【此处一开始监控缺失】 
	- A、B机器Load都很低	
- 软件版本依赖
	- jdk 1.7
	- dubbo 2.5.3
	- Spring 3.2.4
	- webx 3.2
	- dubbo注册中心 zookeeper
	- redis 3.2 	
- 硬件情况
	- 应用服务器 4核8G
	- redis 单机版192G内存，主备同步 

##### 排查详细步骤
1. *观察系统*

	听到这个问题，首先粗略观察下系统，了解下整体架构。接下来观察下服务的性能，发现A调用B的服务，正常情况下，响应时间都在2ms左右。登录到A、B系统的机器上，观察系统状况，发现A、B系统load都不高、内存占用也都良好。
2. 周期性GC问题 ？

	一听到这个现象，想当然就认为，有GC。开心地登录到B系统，查看gc.log，发现，根本就没有Full GC，Young GC也很正常啊。那会不会是A系统周期性GC呢？(Dubbo的超时计时器是在客户端计时的),如果请求发不出去，在客户端就会触发超时。登录到A系统的机器看，发现GC情况也很正常。
	
3. 周期性任务 ？

	周期性任务往往会导致系统负载突然变高。仔细查看A、B的代码和线上日志，发现虽然有周期性任务，但是在周期性任务的时间点，都没有超时发生。
	
	PS：此处对监控系统不熟悉，导致做了很多无用功。完全可以从Zabbix拉出机器的历史LOAD，CPU，内存曲线观察。
	
4. B系统线程池大小不够用 ？
	
	排查中间，向架构师团队寻求咨询。得到思路是，可能B系统dubbo服务线程池不够用，导致线程在服务端排队。毕竟A系统50台机器，B系统只有3台机器。可以加点机器，看看能不能解决。考虑到加机器比较麻烦，先把线程池调成单机400发布。发完后继续观察，发现B系统load确实降低了，但是周期超时问题，还是没有改变。
		
5. 重新思考

	尝试了很多方法，找不到原因后，内心很沮丧。 冷静下来思考，前面的排查，纯粹是凭经验感性地排查，运气好能一击即中，运气不好，完全就是无用功。应该系统性地排查，从源头排查起。

6. 到底是服务端问题，还是客户端问题 ？
	
	首先是确定，到底是服务端问题，还是客户端问题。重新拉取A系统日志，仔细观察发现，在同一时刻，A系统多台机器均出现超时。下面是另一台机器的异常。
	![fp-dubbo-exception-2](http://img.libereco.cn/fp-dubbo-exception-2.png "A系统异常2")
	在这个时刻，A系统的2台机器(192.168.47.104和192.168.47.126)，发起duddo调用，重试了三次，分别重试了B系统的3台机器(192.168.49.105,192.168.49.104,192.168.49.102),全部都出现了超时。再登上A系统的其他机器，发现也都是如此，所有机器，都在同一时刻调用B系统出现大量超时。说明此时，B系统全面超时了。
	
	至此，基本可以排除是A系统问题，断定是B系统服务端问题。

6. 再仔细查看B系统日志
	
	再登上B系统，仔细观察日志(*一行行仔细看*)。突然惊喜发现，2台机器上，均出现了，服务器响应时间过长。而此前的排查，在海量日志中，这几十行被忽略了。
	![titan-response-1](http://img.libereco.cn/titan-response-1.png "B响应时间异常1")
	![titan-response-2](http://img.libereco.cn/titan-response-2.png "B响应时间异常2")
	在同一时刻，多台机器，均出现响应时间飙升，从平时的2ms左右，飙升到1500ms左右。那么，什么可能导致B系统，同一时刻，所有的机器均出现响应时间飙升呢？应该就是他们共同依赖的服务(其他服务、缓存、数据库等)。
	
	至此，基本排除B系统自身问题，断定是依赖外部服务问题。那么，这些查询中，到底依赖了什么外部服务呢？
7. 定位Redis问题
	
	仔细查看代码，发现，在这多个查询中，都用到了redis外部查询。
<pre>
public List<GeoRadiusResponse> georadius(String key, double longitude, double latitude, double radius, GeoUnit unit, GeoRadiusParam param) {
        this.checkIsInMultiOrPipeline();
        this.client.georadius(key, longitude, latitude, radius, unit, param);
        return (List)BuilderFactory.GEORADIUS_WITH_PARAMS_RESULT.build(this.client.getObjectMultiBulkReply());
    }
 </pre>  
 
	难道Redis会周期性性能变差吗？ 查阅相关资料发现，Redis定期刷盘会导致周期性性能变差。
	
	至此，基本确定是Redis周期性刷盘问题导致。
8. 求证
 
 找到DBA，查看Redis主机的配置，果然刷盘策略是(save 900 1 60 1000 600 10000)。即900秒内，只要有1次update，就会触发持久化动作。而我们的系统中，部分从mysql和Cassandra读取到的数据会回写到Redis。
 	
	至此，真相大白。

##### 解决
问题后，解决起来就很简单了。找到DBA，把Redis主库的定时刷盘关掉，保留备库的刷盘。再观察监控，超时消失，问题最终得到解决。

##### 系统架构及代码编写的思考
- 超时设置

处处都应该有超时。这次排查,B系统调用Redis，根本没有设置合理的超时，所以，一开始在B系统上，找不到任何异常日志，给排查工作带到其他沟里去了。

- 监控

完善的监控，对于稳定性及问题排查至关重要。B系统自身服务响应时间的监控缺失，导致定位困难。

##### 排查过程的总结思考
总结起来，几点原因.

- 对基础架构的理解不够深入
- 系统监控不到位
	- 单机监控(cpu,load,gc)
	- 集群监控(tps,rt)【B系统自身服务响应时间监控缺失】
	- 分布式系统监控(Tracer系统)
- 排查思路的摇摆及对日志观察的细致入微程度【问题往往暗藏在蛛丝马迹之中】

##### 相关链接
- [Dubbo](https://github.com/alibaba/dubbo)
- [Redis](http://redis.io)
- [Google Dapper](http://research.google.com/pubs/pub36356.html)
- [Twitter zapkin](https://github.com/openzipkin/zipkin)
- [Redis Persistance](http://redis.io/topics/persistence)
- [美团在Redis上踩过的坑](https://www.google.co.jp/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=%E7%BE%8E%E5%9B%A2+redis+%E5%9D%91)
