Title: 深入理解HttpClient
Date: 2014-11-29 14:00
Modified: 2014-11-29 14:00
Category: Technology
Tags: java,httpClient,http protocal
Slug: deep-understand-http-client
Authors: Estel
Summary: 从HTTP协议的角度，理解Java HttpClient

##### HttpClient是什么
java自身的java.net虽然提供了通过HTTP协议访问资源的基本功能，但是灵活性和功能都不能满足大部分应用的需求。所以[Jakarta Commons HttpClinet](https://hc.apache.org/httpclient-3.x/)模块诞生，期望提供先进高效，有丰富特性的工具包，来满足最新的HTTP协议标准需求。由于扩展性和鲁棒性都很不错，很多网页浏览器，客户端都使用了HttpClient模块。

##### HttpClinet提供的功能
- 执行请求，包括设置URI,Header,Entity,Form参数,异常处理，重试
最简单例子：
```java
CloseableHttpClient httpclient = HttpClients.createDefault();
HttpGet httpget = new HttpGet("http://localhost/");
CloseableHttpResponse response = httpclient.execute(httpget);
try {
    <...>
} finally {
    response.close();
}
```
- 连接维持，路由计算，连接管理(建立，保持，回收)
- Http状态管理，即cookie操作
- Http认证
- 缓存机制，和浏览器类似

##### 生产环境该怎么使用

- 什么是生产环境?
这个不需要解释了吧。生产环境中，我们不能像学习，测试中，随便谢谢，实现功能即可。我们要考虑的是，如果在并发场景下，在占用资源较小的情况下，高性能，高可靠地长期运行。
- 生产环境，我们至少应该该考虑这些吧
> - 连接重用(每次都新建tcp链接的开销可以省去吧)
> - 连接池管理(何时新建连接，何时释放连接,连接池大小设置)
> - 多线程安全(httpclient 是线程安全的吗？)
> - 超时设置(建立连接超时时间，一起请求超时时间，网络抖动下，不能一直等吧)
> - 资源关闭(该close的，是否及时close)

- 这样，代码或许应该这么写才是完备的,注释里有解释
```java
	// 设置线程获取http connection的最大超时时间，如果连接全部被占用，并且在此时间内没有释放，则抛ConnectionPoolTimeoutException
    private static final int         DEFAULT_HTTPCONNECTIONMANAGER_TIMEOUT = 2000;
    // 设置建立连接的超时时间
    private static final int         DEFAULT_CONNECTION_TIMEOUT            = 5000;
    // 设置读超时的时间,即获取response返回的等待时间
    private static final int         DEFAULT_SO_TIMEOUT                    = 5000;
    // 每个Host最大连接数
    private static final int         maxHostConnections                    = 5;
    // 总共的最大连接数
    private static final int         maxTotalConnections                   = 20;

    HttpMethod method = new GetMethod(url);
    try {
         getHttpClient().executeMethod(method);
    } catch (Exception e) {
         logger.error("download file error", e);
    } finally {
    	// 务必要释放连接，可以被其他线程复用
         method.releaseConnection();
    }
        private static HttpClient getHttpClient() {
        if (httpClient == null) {
            httpClient = new HttpClient(new MultiThreadedHttpConnectionManager());
            httpClient.getHttpConnectionManager().getParams().setConnectionTimeout(DEFAULT_CONNECTION_TIMEOUT);
            httpClient.getHttpConnectionManager().getParams().setSoTimeout(DEFAULT_SO_TIMEOUT);
// 设置每个Host最大连接数，默认是2，在并发情况下，等待连接，性能变差            httpClient.getHttpConnectionManager().getParams().setDefaultMaxConnectionsPerHost(maxHostConnections);
            httpClient.getHttpConnectionManager().getParams().setMaxTotalConnections(maxTotalConnections);
//每次都检查连接是否正常，防止Connection Reset
httpClient.getHttpConnectionManager().getParams().setStaleCheckingEnabled(true);
            httpClient.getParams().setConnectionManagerTimeout(DEFAULT_HTTPCONNECTIONMANAGER_TIMEOUT);
        }

        return httpClient;
    }
```

##### 相关链接
1. [HttpClient Tutorial ](https://hc.apache.org/httpcomponents-client-ga/tutorial/html/index.html)
2. [HttpClient Performance Optimize](http://hc.apache.org/httpclient-3.x/performance.html)
3. [RFC 2616](https://www.ietf.org/rfc/rfc2616.txt)




