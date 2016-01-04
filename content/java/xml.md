Title: Java XML
Date: 2016-1-9 14:00
Modified: 2015-1-9 14:00
Category: study
Tags: XML,Java,DOM,SAX,Digester,serialize,json 
Slug: java-xml
Authors: Estel
Summary: Java XML处理技术

###### XML 简介

###### Java XML 解析

从传统上来讲，XML的API无外乎两种：
基于树的API- 整个文档以树的形式被读入内存，可以被调用程序随机访问。
基于事件的API - 应用注册接收事件，当原XML文档遇到事体时就会产生这些事件。

两者皆有优点，前者（例如DOM）允许对文档进行随机访问，而后者（例如SAX）需要较小的内存开销，并却通常更快。
这两个方法可以认为是正好相反。基于树的API允许无限制的，随机的访问和操纵，而基于事件的API是一次性地遍历源文档。
StAX被设计为这两者的一个折中。在StAX中，程序的切入点是表示XML文档中一个位置的光标。应用程序在需要时向前移动光标，从解析器拉出信息。与基于事件的API（如SAX）将“数据推送”给应用程序不同的是，SAX需要应用程序维持时间间的状态，以保持文档内的位置信息。

###### Java XML 解析

###### Java bean to XML

###### 对比Json,Protocal buffer

DOM
SAX
Stax
Digester
Xstream


###### relative link
- [Document Object Model](https://en.wikipedia.org/wiki/Document_Object_Model)
- [Simple API for XML](https://en.wikipedia.org/wiki/Simple_API_for_XML)
- [Stax](https://zh.wikipedia.org/wiki/StAX)
