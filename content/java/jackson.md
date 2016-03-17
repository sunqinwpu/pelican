Title: Jackson导致应用死锁问题
Date: 2016-03-17 14:00
Modified: 2016-03-17 14:00
Category: study
Tags: Java,jackson,LRUMap,Hashmap,LinkedHashmap
Slug: jackson-lock
Authors: Estel
Summary: 一个应用发布重启线程池满问题剖析,Jackson

##### 一个应用发布重启线程池满问题剖析

###### 现象
公司某应用发布的时候，偶尔会有1台机器，出现线程池爆满，CPU使用率飙升到28%左右，找PE重启即可恢复。
发布时，再次发生问题。重启前，jstack dump了机器的堆栈信息。

###### 环境
- OS linux
- JDK 1.6
- Jackson 2.4.1
- 服务框架线程池大小默认400

###### 排查过程
1.	老方法，分析堆栈信息。发现大量线程卡住在com.fasterxml.jackson.databind.util.LRUMap.get处等待锁,共有399个。
```java
"HSFBizProcessor-4-thread-400" prio=10 tid=0x00007f4ae80c4800 nid=0x5e36 waiting on condition [0x00007f4ad64fc000]
   java.lang.Thread.State: WAITING (parking)
    at sun.misc.Unsafe.park(Native Method)
    - parking to wait for  <0x0000000756e00130> (a java.util.concurrent.locks.ReentrantReadWriteLock$NonfairSync)
    at java.util.concurrent.locks.LockSupport.park(LockSupport.java:156)
    at java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt(AbstractQueuedSynchronizer.java:811)
    at java.util.concurrent.locks.AbstractQueuedSynchronizer.doAcquireShared(AbstractQueuedSynchronizer.java:941)
    at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquireShared(AbstractQueuedSynchronizer.java:1261)
    at java.util.concurrent.locks.ReentrantReadWriteLock$ReadLock.lock(ReentrantReadWriteLock.java:594)
    at com.fasterxml.jackson.databind.util.LRUMap.get(LRUMap.java:56)
    at com.fasterxml.jackson.databind.type.TypeFactory._fromClass(TypeFactory.java:707)
    at com.fasterxml.jackson.databind.type.TypeFactory._constructType(TypeFactory.java:387)
    at com.fasterxml.jackson.databind.type.TypeFactory.constructType(TypeFactory.java:354)
    at com.fasterxml.jackson.databind.ObjectMapper.readValue(ObjectMapper.java:2146)
    at com.alipay.baoxianapi.client.util.JacksonUtil.jsonToBean(JacksonUtil.java:58)
```
另外，还有1个线程卡住在com.fasterxml.jackson.databind.util.LRUMap.put处。
```java
"HSFBizProcessor-4-thread-11" prio=10 tid=0x00007f4afc019000 nid=0x581e runnable [0x00007f4ae3212000]
   java.lang.Thread.State: RUNNABLE
    at java.util.LinkedHashMap.transfer(LinkedHashMap.java:234)
    at java.util.HashMap.resize(HashMap.java:463)
    at java.util.LinkedHashMap.addEntry(LinkedHashMap.java:414)
    at java.util.HashMap.put(HashMap.java:385)
    at com.fasterxml.jackson.databind.util.LRUMap.put(LRUMap.java:68)
    at com.fasterxml.jackson.databind.type.TypeFactory._fromClass(TypeFactory.java:738)
    at com.fasterxml.jackson.databind.type.TypeFactory._constructType(TypeFactory.java:387)
    at com.fasterxml.jackson.databind.type.TypeFactory.constructType(TypeFactory.java:358)
    at com.fasterxml.jackson.databind.cfg.MapperConfig.constructType(MapperConfig.java:268)
    at com.fasterxml.jackson.databind.cfg.MapperConfig.introspectClassAnnotations(MapperConfig.java:298)
    at com.fasterxml.jackson.databind.deser.BeanDeserializerFactory.isIgnorableType(BeanDeserializerFactory.java:867)
    at com.fasterxml.jackson.databind.deser.BeanDeserializerFactory.filterBeanProps(BeanDeserializerFactory.java:635)
    at com.fasterxml.jackson.databind.deser.BeanDeserializerFactory.addBeanProps(BeanDeserializerFactory.java:527)
    at com.fasterxml.jackson.databind.deser.BeanDeserializerFactory.buildBeanDeserializer(BeanDeserializerFactory.java:270)
    at com.fasterxml.jackson.databind.deser.BeanDeserializerFactory.createBeanDeserializer(BeanDeserializerFactory.java:168)
    at com.fasterxml.jackson.databind.deser.DeserializerCache._createDeserializer2(DeserializerCache.java:399)
    at com.fasterxml.jackson.databind.deser.DeserializerCache._createDeserializer(DeserializerCache.java:348)
    at com.fasterxml.jackson.databind.deser.DeserializerCache._createAndCache2(DeserializerCache.java:261)
    at com.fasterxml.jackson.databind.deser.DeserializerCache._createAndCacheValueDeserializer(DeserializerCache.java:241)
    - locked <0x000000075766b060> (a java.util.HashMap)
    at com.fasterxml.jackson.databind.deser.DeserializerCache.findValueDeserializer(DeserializerCache.java:142)
    at com.fasterxml.jackson.databind.DeserializationContext.findContextualValueDeserializer(DeserializationContext.java:367)
    at com.fasterxml.jackson.databind.deser.std.CollectionDeserializer.createContextual(CollectionDeserializer.java:152)
    at com.fasterxml.jackson.databind.deser.std.CollectionDeserializer.createContextual(CollectionDeserializer.java:25)
    at com.fasterxml.jackson.databind.DeserializationContext.handleSecondaryContextualization(DeserializationContext.java:581)
    at com.fasterxml.jackson.databind.DeserializationContext.findContextualValueDeserializer(DeserializationContext.java:369)
    at com.fasterxml.jackson.databind.deser.std.StdDeserializer.findDeserializer(StdDeserializer.java:842)
    at com.fasterxml.jackson.databind.deser.BeanDeserializerBase.resolve(BeanDeserializerBase.java:438)
    at com.fasterxml.jackson.databind.deser.DeserializerCache._createAndCache2(DeserializerCache.java:292)
    at com.fasterxml.jackson.databind.deser.DeserializerCache._createAndCacheValueDeserializer(DeserializerCache.java:241)
    - locked <0x000000075766b060> (a java.util.HashMap)
    at com.fasterxml.jackson.databind.deser.DeserializerCache.findValueDeserializer(DeserializerCache.java:142)
    at com.fasterxml.jackson.databind.DeserializationContext.findRootValueDeserializer(DeserializationContext.java:381)
    at com.fasterxml.jackson.databind.ObjectMapper._findRootDeserializer(ObjectMapper.java:3154)
    at com.fasterxml.jackson.databind.ObjectMapper._readMapAndClose(ObjectMapper.java:3047)
    at com.fasterxml.jackson.databind.ObjectMapper.readValue(ObjectMapper.java:2146)
    at com.alipay.baoxianapi.client.util.JacksonUtil.jsonToBean(JacksonUtil.java:58)
```
第一想法，此LRUMap的实现有问题，导致了死锁。
2.	于是扒代码看看。LRUMap部分代码如下：
```java
public class LRUMap<K,V> extends LinkedHashMap<K,V>
    implements java.io.Serializable
{
    private static final long serialVersionUID = 1L;

    protected final transient Lock _readLock, _writeLock;
    
    protected final transient int _maxEntries;
    
    public LRUMap(int initialEntries, int maxEntries)
    {
        super(initialEntries, 0.8f, true);
        _maxEntries = maxEntries;
        final ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
        _readLock = rwl.readLock();
        _writeLock = rwl.writeLock();
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K,V> eldest) {
        return size() > _maxEntries;
    }

    /*
    /**********************************************************
    /* Overrides to support proper concurrency
    /**********************************************************
     */

    @Override
    public V get(Object key) {
        _readLock.lock();
        try {
            return super.get(key);
        } finally {
            _readLock.unlock();
        }
    }

    @Override
    public V put(K key, V value) {
        _writeLock.lock();
        try {
            return super.put(key, value);
        } finally {
            _writeLock.unlock();
        }
    }

    @Override
    public V remove(Object key) {
        _writeLock.lock();
        try {
            return super.remove(key);
        } finally {
            _writeLock.unlock();
        }
    }

    /**
     * Overridden to allow concurrent way of removing all cached entries.
     * 
     * @since 2.4.1
     */
    @Override
    public void clear() {
        _writeLock.lock();
        try {
            super.clear();
        } finally {
            _writeLock.unlock();
        }
    }
```
反复看了很久这里的代码，基于可重入读写锁的设计控制，完全没有死锁的可能性。
3. 就在即将放弃的时候，想起了Hashmap并发更新的问题。再仔细看了下堆栈信息。399个线程都在等待读锁，1个线程获取了写锁，很合理。
这才发现，问题的关键不在于死锁，而在于为什么这个获取写锁的线程，迟迟没有完成写操作，释放锁退出。也就是，为什么会卡在LinkedHashMap.transfer这个方法这里？
```java
"HSFBizProcessor-4-thread-11" prio=10 tid=0x00007f4afc019000 nid=0x581e runnable [0x00007f4ae3212000]
   java.lang.Thread.State: RUNNABLE
    at java.util.LinkedHashMap.transfer(LinkedHashMap.java:234)
    at java.util.HashMap.resize(HashMap.java:463)
    at java.util.LinkedHashMap.addEntry(LinkedHashMap.java:414)
    at java.util.HashMap.put(HashMap.java:385)
    at com.fasterxml.jackson.databind.util.LRUMap.put(LRUMap.java:68)
    at
```
4.	找到LinkedHashMap的源码(线上JDK是1.6),源码如下：
```java
    /**
     * Transfers all entries to new table array.  This method is called
     * by superclass resize.  It is overridden for performance, as it is
     * faster to iterate using our linked list.
     */
    void transfer(HashMap.Entry[] newTable) {
        int newCapacity = newTable.length;
        for (Entry<K,V> e = header.after; e != header; e = e.after) {
            int index = indexFor(e.hash, newCapacity);
            e.next = newTable[index];
            newTable[index] = e;
        }
    }
```
这里反复读了很久，功能也很简单，就是Hashmap的resize操作，又没有锁，不至于卡住在这里啊。
5.	又仔细回忆下，想起了一个问题，Hashmap在并发更新，并resize的情况下，极端情况会导致内部链表产生环，进而会导致读写操作死循环。难道这个Hashmap被并发更新了吗？ 再仔细分析LRUMap的源代码，发现，在写操作的时候，都有写锁保护了，不会出现并发更新啊。
6. 那么问题究竟是怎么产生的呢？再分析LRUMap的源码，它继承了LinkedHashMap。LinkedHashmap在内部维护了1个双向列表，用于对元素进行排序。可以根据插入顺序排序或者访问顺序排序。看下LinkedHashMap的源码。
```java
    /**
     * Returns the value to which the specified key is mapped,
     * or {@code null} if this map contains no mapping for the key.
     *
     * <p>More formally, if this map contains a mapping from a key
     * {@code k} to a value {@code v} such that {@code (key==null ? k==null :
     * key.equals(k))}, then this method returns {@code v}; otherwise
     * it returns {@code null}.  (There can be at most one such mapping.)
     *
     * <p>A return value of {@code null} does not <i>necessarily</i>
     * indicate that the map contains no mapping for the key; it's also
     * possible that the map explicitly maps the key to {@code null}.
     * The {@link #containsKey containsKey} operation may be used to
     * distinguish these two cases.
     */
    public V get(Object key) {
        Entry<K,V> e = (Entry<K,V>)getEntry(key);
        if (e == null)
            return null;
        e.recordAccess(this);
        return e.value;
    }
    /**
     * LinkedHashMap entry.
     */
    private static class Entry<K,V> extends HashMap.Entry<K,V> {
        // These fields comprise the doubly linked list used for iteration.
        Entry<K,V> before, after;

	Entry(int hash, K key, V value, HashMap.Entry<K,V> next) {
            super(hash, key, value, next);
        }

        /**
         * Removes this entry from the linked list.
         */
        private void remove() {
            before.after = after;
            after.before = before;
        }

        /**
         * Inserts this entry before the specified existing entry in the list.
         */
        private void addBefore(Entry<K,V> existingEntry) {
            after  = existingEntry;
            before = existingEntry.before;
            before.after = this;
            after.before = this;
        }

        /**
         * This method is invoked by the superclass whenever the value
         * of a pre-existing entry is read by Map.get or modified by Map.set.
         * If the enclosing Map is access-ordered, it moves the entry
         * to the end of the list; otherwise, it does nothing.
         */
        void recordAccess(HashMap<K,V> m) {
            LinkedHashMap<K,V> lm = (LinkedHashMap<K,V>)m;
            if (lm.accessOrder) {
                lm.modCount++;
                remove();
                addBefore(lm.header);
            }
        }

        void recordRemoval(HashMap<K,V> m) {
            remove();
        }
    }
```
当选定按照访问顺序排序的情况下，每次get都会操作，把最近访问的元素放到链表的开头。所以，问题的根结在于LinkedHashMap的get方法会改变数据链表，每次都会把1个元素放到表头，并发情况下，会形成环。

7.	LinkedHashmap内部形成了环，导致了在resize的时候，根据链表遍历元素，拷贝到新的table的时候，死循环。线上4核机器，1个核跑满，cpu使用率超过25%。看如下代码，通过这个header遍历的时候，链表有环。
```java
    /**
     * Transfers all entries to new table array.  This method is called
     * by superclass resize.  It is overridden for performance, as it is
     * faster to iterate using our linked list.
     */
    void transfer(HashMap.Entry[] newTable) {
        int newCapacity = newTable.length;
        for (Entry<K,V> e = header.after; e != header; e = e.after) {
            int index = indexFor(e.hash, newCapacity);
            e.next = newTable[index];
            newTable[index] = e;
        }
    }
```
8.	每次机器重启的时候，大量请求进入，LRUMap初始化，最容易爆发问题。

###### 解决方案
- 抓紧升级jackson到更新的版本。jackson新版本中，已经抛弃了这个LRUMap。不然，以后发布的时候，还是会有可能发生问题。
- 强烈建议抛弃jackson，直接使用fastjason。

###### 附录
- Hashmap并发put导致死循环问题，参考[http://coolshell.cn/articles/9606.html](http://coolshell.cn/articles/9606.html)
- LinkedHashmap的坑 [http://www.blogjava.net/aoxj/archive/2012/06/18/381001.html](http://www.blogjava.net/aoxj/archive/2012/06/18/381001.html)
