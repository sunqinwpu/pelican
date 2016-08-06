Title: Dubbo服务周期性超时问题排查
Date: 2016-08-05 14:00
Modified: 2016-08-05 14:00
Category: java
Tags: Java,Dubbo,Timeout,Redis,刷盘 
Slug: dubbo-timeout-redis
Authors: Estel
Summary: Dubbo服务周期性超时问题排查思路，最终定位为Redis周期性刷盘导致。排查过程值得思考

##### 问题背景
新公司入职、接手的系统有个奇怪的现象，A系统通过Dubbo服务调用B系统，每隔十几分钟就出现大量的超时。对这种问题，也算是见多识广，不过这次排查也着实耗费了不少精力。


##### 总结
总结起来，几点原因.

- 对基础架构的理解不够深入
- 系统监控不到位
	- 单机监控(cpu,load,gc)
	- 集群监控(tps,rt)
	- 分布式系统监控(Tracer系统)
- 排查思路的摇摆及对日志观察的细致入微程度

##### Java
- [Dubbo](https://github.com/alibaba/dubbo)
- [Redis](http://redis.io)
- [Google Dapper](http://research.google.com/pubs/pub36356.html)
- [Twitter zapkin](https://github.com/openzipkin/zipkin)

###### relative link
