Title: Redis实现有序队列及实际应用
Date: 2016-10-09 14:00
Modified: 2016-10-09 14:00
Category: Technology
Tags: redis,有序队列, sortedset
Slug: redis-sorted-queue 
Authors: Estel
Summary: redis是一个简单的kv数据库，利用redis支持的list、set等数据结构，可以很方便地实现有序队列

##### 概述
业务中经常需要用到并发和多线程控制。在java中，有PriorityQueue，BlockingQueue等队列。在分布式环境下，要实现类似java的PriorityQueue，BlockingQueue，有多种方案。Redis是一个开源的内存存储，可以用作数据库、缓存和消息系统。利用redis支持的list、set等数据结构，可以很方便地实现有序队列。

##### 实现方案
redis自带的sortedset是有序集合。

- 集合操作方法zadd添加时，将score比做是优先级，也可以用时间戳来当做score，用来表示时间。

- 集合操作方法，ZREVRANGE key start stop [WITHSCORES] 
返回有序集中指定区间内的成员，通过索引，分数从高到底

- 集合操作方法，ZREMRANGEBYSCORE key min max 
移除有序集合中给定的分数区间的所有成员

通过上述的添加、查询和移除，可以实现消息队列的插入和弹出。

##### 实际应用场景
在公司的业务中，有ip代理扫描的需求，即判断一个ip是否是代理。具体实现如下：

- 新增一个待扫描ip队列，一个扫描结果ip队列
- 新ip到来的时候，先查询扫描结果队列，看是否存在该ip；如果不存在，则提交到待扫描队列中，score用插入时间代替
- 消费者消费待扫描队列出的ip，先入先出

##### 总结
用redis实现，简单易用。
但是，有一个潜在的问题，当取出ip，还没有做完业务逻辑，抛出异常或者机器重启，是无法重试的。对于高可用场景，还需要进一步优化。

##### relative link
- [Redis](http://redis.io/)
- [基于redis构建消息队列](http://lanjingling.github.io/2016/01/29/messagequeue-redis/)
