Title: Java问题排查利器(从Btrace到Greys)
Date: 2017-09-20 14:00
Modified: 2015-09-20 14:00
Category: javax
Tags: Java,Btrace,Greys 
Slug: btrace-greys
Authors: Estel
Summary:
线上性能不时抖动，功能偶尔突发异常，排查之路道阻且长。怎么办？无奈地想办法直接连接线上debug，频繁的在关键节点增删日志，无语地频繁发布。Btrace作为在线排查问题的利器，可以方便地在线动态调试，功能强大。然而，强大之余，一不小心，出个错，就会对线上系统产生致命影响。在Btrace的基础上，淘宝的同学开发了HouseMD，后来又发展出Greys-Anatomy。本文，从java源头讲起，带大家一起看下Java在线问题排查之路。

##### 前言
线上性能不时抖动，功能偶尔突发异常，排查之路道阻且长。怎么办？无奈地想办法直接连接线上debug?频繁的在关键节点增删日志?无语地频繁发布?如果能在线，按照自己的意愿，动态地在某些方法上，打印log，添加监控，查看变量，又不影响程序的正常对外提供服务，何其美妙。本文通过梳理java对在线监控的支持，btrace，houseMD,greys-anatomy等工具，回顾总结下java问题在线排查利器。

##### 技术基础
- Java Instrument API
Java Instrument API允许java程序，通过代理的方式，加载一个agent的jar。这个jar可以通过修改字节码的方式，替换现有程序的实现逻辑。

例如如下的Agent,可以添加一个TestTransformer。

```java
package test;  
  
import java.lang.instrument.Instrumentation;  
  
public class Agent {  
  
    public static void premain(String args, Instrumentation inst){  
        System.out.println("Hi, I'm agent!");  
        inst.addTransformer(new TestTransformer());  
    }  
}  
```

TestTransformer可以有多种实现，比如如下实现，可以在方法开始出添加了一段打印该类名和方法名的字节码。

```java
public class TestTransformer implements ClassFileTransformer {  
  
    @Override  
    public byte[] transform(ClassLoader arg0, String arg1, Class<?> arg2,  
            ProtectionDomain arg3, byte[] arg4)  
            throws IllegalClassFormatException {  
        ClassReader cr = new ClassReader(arg4);  
        ClassNode cn = new ClassNode();  
        cr.accept(cn, 0);  
        for (Object obj : cn.methods) {  
            MethodNode md = (MethodNode) obj;  
            if ("<init>".endsWith(md.name) || "<clinit>".equals(md.name)) {  
                continue;  
            }  
            InsnList insns = md.instructions;  
            InsnList il = new InsnList();  
            il.add(new FieldInsnNode(Opcodes.GETSTATIC, "java/lang/System",  
                    "out", "Ljava/io/PrintStream;"));  
            il.add(new LdcInsnNode("Enter method-> " + cn.name+"."+md.name));  
            il.add(new MethodInsnNode(Opcodes.INVOKEVIRTUAL,  
                    "java/io/PrintStream", "println", "(Ljava/lang/String;)V"));  
            insns.insert(il);  
            md.maxStack += 3;  
  
        }  
        ClassWriter cw = new ClassWriter(0);  
        cn.accept(cw);  
        return cw.toByteArray();  
    }  
}  
```
编写MANIFEST.MF

```java
Manifest-Version: 1.0  
Premain-Class: test.Agent  
Created-By: 1.8.0_91  
```
代码编译后打包成Agent.jar。随便写个测试类。执行

```java
java -javaagent:agent.jar TestAgent  
```
可以看到打印出

```java
Hi, I'm agent!  
Enter method-> test/TestAgent.main  
Enter method-> test/TestAgent.test  
I'm TestAgent  
Enter method-> java/util/IdentityHashMap$KeySet.iterator  
Enter method-> java/util/IdentityHashMap$IdentityHashMapIterator.hasNext  
Enter method-> java/util/IdentityHashMap$KeyIterator.next  
Enter method-> java/util/IdentityHashMap$IdentityHashMapIterator.nextIndex  
Enter method-> java/util/IdentityHashMap$IdentityHashMapIterator.hasNext 
...
```

在java se5 时代，Instrument只提供了premain一种方式，即在真正的应用程序（包含main方法的程序）main方法启动前启动一个代理程序。在代理程序中，可以修改现有类的字节码。字节码不能随便乱改，不然程序就改挂了！

- Java Attach API

通过Instrument API，可以在程序运行时，加载agent jar。 如果想在程序启动之后开启代理，怎么办呢？Java Attach API 提供了一个本地虚拟机挂载程序，可以连接到正在运营的JVM，并且可以通过loadAgent方法，加载一个本地的agent jar到远程JVM。

编写Agent的方式和上面一样，加载可以通过如下方式加载。该程序接受一个参数为目标应用程序的进程id，通过Attach Tools API的VirtualMachine.attach方法绑定到目标VM，并向其中加载代理jar。

```java
public class Test {
    public static void main(String[] args) throws AttachNotSupportedException,
            IOException, AgentLoadException, AgentInitializationException {
        VirtualMachine vm = VirtualMachine.attach(args[0]);
        vm.loadAgent("Agent.jar");
    }
}
```

- ASM
ASM是一个java字节码分析修改框架，提供了基础的字节码核心分析和转换方法，可以动态地修改现有类或者动态生成新类。不过使用ASM分析类，需要对JVM规范非常熟悉，有一定的门槛。
- Byte Buddy
Byte Buddy是一个依赖ASM的java类分析修改框架，但是更简单易用。使用Byte Buddy不需要理解java字节码或者class文件格式。Byte Buddy设计目标就是让每个人都易于理解。一个简单的例子如下：

```java
Class<?> dynamicType = new ByteBuddy()
  .subclass(Object.class)
  .method(ElementMatchers.named("toString"))
  .intercept(FixedValue.value("Hello World!"))
  .make()
  .load(getClass().getClassLoader())
  .getLoaded();
 
assertThat(dynamicType.newInstance().toString(), is("Hello World!"));
```

- JMX
JMX 就是一套可以在运行时获取大多数 JVM 状态的接口，比如 GC、线程、ClassLoading 信息等。

##### Btrace
通过上面的技术基础的了解，可以看到，有很多工具都能让我们对运行中的JVM程序进行动态调试。但是，有2点不便的地方 ：

1. 成本很高。 需要熟悉java字节码，需要写类转换的代码。
2. 安全性很差。 如果一不小心，在字节码的修改上出了问题，就会导致线上运行的程序，直接出bug。

有没有一种方便，安全的方法，对运行中的JVM程序进行动态调试呢？ Btrace就是这么一款利器。

Btrace基于ASM实现，可以通过插入追踪代码的方式，动态地监控目标程序的类。Btrace的特点是:

- 无侵入性。 无需我们队原有代码做任何修改，通过注解的方式，完成跟踪类的监控。
- 不修改应用任何数据。无需重启目标java进程，动态加载agent。
举一个简单的例子，比如我们有一个Hello.java

```java
public class Hello {

    public String sayHello() {
        try {
            Thread.sleep(100);
        } catch (Exception e) {
        }
        return "Hello, time : " + new Date();
    }
}
```
通过HelloTest.java来运行。

```java
public class HelloTest {

    public static void main(String[] args) {
        try {
            new HelloTest().testHello();
        } catch (Exception e) {
        }
    }

    public void testHello() throws InterruptedException {
        for (int i = 0; i < 100; i++) {
            String value = new Hello().sayHello();
            System.out.println(value);
            Thread.sleep(2000);
        }
    }
}
```
为了监控Hello.java的sayHello运行情况，我们可以使用如下的BtraceHello.java

```java
@BTrace
public class BtraceHello {

    @TLS
    private static long startTime;

    @OnMethod(clazz = "org.dolphin.study.java.btrace.Hello", method = "sayHello")
    public static void startSayHello() {
        startTime = BTraceUtils.currentThreadCpuTime();
    }

    @OnMethod(clazz = "org.dolphin.study.java.btrace.Hello", method = "sayHello", location = @Location(Kind.RETURN))
    public static void traceSayHello(@ProbeMethodName String probeMethodName) {
        BTraceUtils.println("interval : " + (BTraceUtils.currentThreadCpuTime() - startTime));
        BTraceUtils.println("probeMethodName : " + probeMethodName);
    }
}
```
通过命令java HelloTest运行HelloTest后，可以使用Btrace进行监控

```java
./btrace 40785 ~/study/java-common/src/main/java/org/dolphin/study/java/btrace/BtraceHello.java
interval : 361000
probeMethodName : sayHello
interval : 188000
probeMethodName : sayHello
interval : 253000
probeMethodName : sayHello
interval : 214000
probeMethodName : sayHello
interval : 192000
probeMethodName : sayHello
interval : 212000
probeMethodName : sayHello
```
这里打印出了执行时间和执行的方法名。 当然Btrace还可以打印出参数，返回值等等。值得一提的是，Btrace为了保护运行中的应用程序，不被修改，规定只允许使用BTraceUtils的方法进行操作。

##### HouseMD
2012年淘宝的聚石用scala写了HouseMD，将常用的几个Btrace脚本整合在一起形成一个独立风格的应用。简单易用，不需要写任何代码，就可以直接完成上面Btrace解决方案中，需要写java代码才能完成的事情。 可惜现在项目已经不再维护了，不过，在这个项目的启发下，诞生了Greys-Anatomy。

##### Greys-Anatomy
Greys是一个JVM进程执行过程中的异常诊断工具，可以在不中断程序执行的情况下轻松完成问题排查工作。和Btrace不同的地方是，使用Greys根本不需要编程，只需要通过一些简单的命令，就可以完成上面的工作。

```java
bin git:(master) ✗ ./greys.sh 41809@127.0.0.1:6666
                                                        _
  ____  ____ _____ _   _  ___ _____ _____ ____  _____ _| |_ ___  ____  _   _
 / _  |/ ___) ___ | | | |/___|_____|____ |  _ \(____ (_   _) _ \|    \| | | |
( (_| | |   | ____| |_| |___ |     / ___ | | | / ___ | | || |_| | | | | |_| |
 \___ |_|   |_____)\__  (___/      \_____|_| |_\_____|  \__)___/|_|_|_|\__  |
(_____|           (____/                                              (____/
                                              +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                                              |v|e|r|s|i|o|n|:|1|.|7|.|6|.|4|
                                              +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
ga?>
ga?>monitor -c 5 org.dolphin.study.java.btrace.Hello sayHello
Press Ctrl+D to abort.
Affect(class-cnt:1 , method-cnt:1) cost in 134 ms.
+-----------+-------+--------+-------+---------+------+-----------+------------+------------+------------+
| TIMESTAMP | CLASS | METHOD | TOTAL | SUCCESS | FAIL | FAIL-RATE | AVG-RT(ms) | MIN-RT(ms) | MAX-RT(ms) |
+-----------+-------+--------+-------+---------+------+-----------+------------+------------+------------+

+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+
| TIMESTAMP           | CLASS                               | METHOD   | TOTAL | SUCCESS | FAIL | FAIL-RATE | AVG-RT(ms) | MIN-RT(ms) | MAX-RT(ms) |
+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+
| 2017-09-21 19:52:24 | org.dolphin.study.java.btrace.Hello | sayHello | 2     | 2       | 0    | 00.00%    | 103.00     | 102        | 104        |
+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+

+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+
| TIMESTAMP           | CLASS                               | METHOD   | TOTAL | SUCCESS | FAIL | FAIL-RATE | AVG-RT(ms) | MIN-RT(ms) | MAX-RT(ms) |
+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+
| 2017-09-21 19:52:29 | org.dolphin.study.java.btrace.Hello | sayHello | 3     | 3       | 0    | 00.00%    | 104.67     | 103        | 106        |
+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+

+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+
| TIMESTAMP           | CLASS                               | METHOD   | TOTAL | SUCCESS | FAIL | FAIL-RATE | AVG-RT(ms) | MIN-RT(ms) | MAX-RT(ms) |
+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+
| 2017-09-21 19:52:34 | org.dolphin.study.java.btrace.Hello | sayHello | 2     | 2       | 0    | 00.00%    | 103.50     | 102        | 105        |
+---------------------+-------------------------------------+----------+-------+---------+------+-----------+------------+------------+------------+
```
如上图，直接一行命令就可以完成对一个方法的监控。

##### 总结
如果出现在线问题，线下无法复现，需要排查，Greys-Anatomy是一个非常好的选择。 如果Greys-Anatomy现有方法不能满足，Btrace应该可以满足。

##### 相关链接
- [Java Instrument](https://docs.oracle.com/javase/8/docs/api/java/lang/instrument/package-summary.html)
- [Java Attach](http://docs.oracle.com/javase/7/docs/technotes/guides/attach/index.html)
- [ASM](http://asm.ow2.org/)
- [Byte Buddy](http://bytebuddy.net/)
- [Btrace](https://github.com/btraceio/btrace)
- [HouseMd](https://github.com/CSUG/HouseMD)
- [Greys-Anatomy](https://github.com/oldmanpushcart/greys-anatomy)
