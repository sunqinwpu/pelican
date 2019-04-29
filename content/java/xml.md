Title: Java XML
Date: 2016-01-20 14:00
Modified: 2015-01-20 14:00
Category: Technology
Tags: XML,Java,DOM,SAX,Digester,serialize,json
Slug: java-xml
Authors: Estel
Summary: Java XML处理技术

###### XML 简介

###### Java XML 解析

&#160; &#160; &#160; &#160;从传统上来讲，XML的API无外乎两种：
- 基于树的API- 整个文档以树的形式被读入内存，可以被调用程序随机访问。
- 基于事件的API - 应用注册接收事件，当原XML文档遇到事体时就会产生这些事件。

&#160; &#160; &#160; &#160;两者皆有优点，前者（例如DOM）允许对文档进行随机访问，而后者（例如SAX）需要较小的内存开销，并却通常更快。

&#160; &#160; &#160; &#160;这两个方法可以认为是正好相反。基于树的API允许无限制的，随机的访问和操纵，而基于事件的API是一次性地遍历源文档。

&#160; &#160; &#160; &#160;StAX被设计为这两者的一个折中。在StAX中，程序的切入点是表示XML文档中一个位置的光标。应用程序在需要时向前移动光标，从解析器拉出信息。与基于事件的API（如SAX）将“数据推送”给应用程序不同的是，StAX需要应用程序维持时间间的状态，以保持文档内的位置信息。

###### Java XML 解析
&#160; &#160; &#160; &#160; 基于上文所述的理论，JAVA XML解析，比较流行的有。DOM,SAX,JDOM,Dom4j。具体如下。
&#160; &#160; &#160; &#160;以如下xml解析为例:
```XML
 <?xml version="1.0" encoding="UTF-8"?> 
 <books> 
   <book id="001"> 
      <title>野心时代</title> 
      <author>Evan Osnos</author> 
   </book> 
   <book id="002"> 
      <title>禅者的初心</title> 
      <author>铃木俊隆</author> 
   </book> 
 </books>
```

- DOM(Document Object Model)。 DOM是平台无关的表示XML文档的W3C标准，以层次结构组织文档信息。用DOM分析，需要把整个文档加载并构造层次结构。带来的优点是：
	- 可以快速随机访问文档中的任意数据
	- 允许应用程序对数据和结构做出更改。
随之而来的缺点是：
	- 资源消耗很大(要全部加载到内存中)。
示例代码：

```java
public class DomTest {
    /** */
    private static Logger logger = LogManager.getLogger(DomTest.class);

    /**
     * 测试
     */
    @Test
    public void testDomParse() {
        try {
            DocumentBuilderFactory builderFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = builderFactory.newDocumentBuilder();
            InputStream inputStream = DomTest.class.getClassLoader().getResourceAsStream(
                "xml/books.xml");
            Document document = builder.parse(inputStream);
            Element rootElement = document.getDocumentElement();
            NodeList nodes = rootElement.getChildNodes();
            for (int i = 0; i < nodes.getLength(); i++) {
                Node node = nodes.item(i);
                if (node.getNodeType() == Node.ELEMENT_NODE) {
                    Element child = (Element) node;
                    String id = child.getAttribute("id");
                    logger.info(id);
                    NodeList nodeList = child.getChildNodes();
                    for (int j = 0; j < nodeList.getLength(); j++) {
                        Node valueNode = nodeList.item(j);
                        if (StringUtils.equals(valueNode.getNodeName(), "title")) {
                            String title = valueNode.getChildNodes().item(0).getNodeValue();
                            logger.info("title:" + title);
                        }
                        if (StringUtils.equals(valueNode.getNodeName(), "author")) {
                            String title = valueNode.getChildNodes().item(0).getNodeValue();
                            logger.info("title:" + title);
                        }
                    }
                }
            }

            NodeList nodeList = rootElement.getElementsByTagName("book");
            if (nodeList != null) {
                for (int i = 0; i < nodeList.getLength(); i++) {
                    Element element = (Element) nodeList.item(i);
                    String id = element.getAttribute("id");
                    logger.info(id);
                    // 同上
                }
            }
        } catch (Exception e) {
            logger.error("parse exception", e);
        }
    }
}
```
- SAX(Simple API for XML)。SAX解析器采用了基于事件的模型，它在解析XML文档的时候可以触发一系列的事件，无需加载整个文档到内存中。显然，优点很多：
	- 占用内存小，性能和效率高
	- 必须遍历整个文档
缺点就是：
	- 无法定位文档层次，无法随机访问
	- 复杂，其实也不算太复杂，需要自己定制Tag关系
示例代码：
	解析类需要继承DefaultHandler，并覆盖其中对应的方法。
    
```java
public class SAXTest {
    /** */
    private static Logger logger = LogManager.getLogger(DomTest.class);

    /**
     * 测试SAX解析XML
     */
    @Test
    public void testSaxParse() {
        try {
            InputStream inputStream = DomTest.class.getClassLoader().getResourceAsStream(
                "xml/books.xml");
            SAXParserFactory factory = SAXParserFactory.newInstance();
            SAXParser parser = factory.newSAXParser();
            parser.parse(inputStream, new BooksHandler());
        } catch (Exception e) {
            logger.error("parse exception", e);
        }
    }
}

class BooksHandler extends DefaultHandler {
    /** */
    private static Logger logger = LogManager.getLogger(DomTest.class);

    @Override
    public void startDocument() throws SAXException {
        logger.info("start document");
    }

    @Override
    public void endDocument() throws SAXException {
        logger.info("end document");
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes)
                                                                                               throws SAXException {
        logger.info("start element, uri:" + uri + ",localName:" + localName + ",qName:" + qName);
        for (int i = 0; i < attributes.getLength(); i++) {
            logger
                .info("attributes qName:" + attributes.getQName(i) + ":" + attributes.getValue(i));
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName) throws SAXException {
        logger.info("end element, uri:" + uri + ",localName:" + localName + ",qName:" + qName);
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        logger.info("element value:" + new String(ch, start, length));
    }
}
```

- JDOM
  JDOM也是基于Document模型的，只不过，作为新一代的工具，提供了更简单易用的API。
  
```java
public class JDomTest {
    /** */
    private static Logger logger = LogManager.getLogger(JDomTest.class);

    /**
     *
     */
    @Test
    public void testJdomParse() {
        try {
            InputStream inputStream = DomTest.class.getClassLoader().getResourceAsStream(
                "xml/books.xml");
            SAXBuilder saxBuilder = new SAXBuilder();
            Document document = saxBuilder.build(inputStream);
            Element books = document.getRootElement();
            logger.info("books name:" + books.getName());
            List<Element> bookList = books.getChildren();
            for (Element element : bookList) {
                logger.info("book attribute id:" + element.getAttributeValue("id"));
                List<Element> childElements = element.getChildren();
                for (Element childElement : childElements) {
                    logger.info("book child " + childElement.getName() + ",value:"
                                + childElement.getText());
                }
            }
        } catch (Exception e) {
            logger.error("parse error", e);
        }
    }
}
```

- Dom4j
  同上，类似，也是基于DOM的处理器，使用SAXReader处理xml。不做赘述。
- StAX
上面介绍的4种XML处理方式都是JDK6.0之前提供的工具。StAX(Streaming Api for XML)是JDK6.0新提供的XML解析工具，是一种针对XML的流式拉分析API。如同SAX一样，StAX也是基于流的模型，流模型分2类：
	- 推模型：就是我们常说的SAX，它是一种靠事件驱动的模型。当它每发现一个节点就引发一个事件，而我们需要编写这些事件的处理程序。这样的做法很麻烦，且不灵活。
	- 拉模型：在遍历文档时，会把感兴趣的部分从读取器中拉出，不需要引发事件，允许我们选择性地处理节点。这大大提高了灵活性，以及整体效率。

```java
public class StAXTest {
    /** */
    private static Logger logger = LogManager.getLogger(DomTest.class);

    /**
     * 测试SAX解析XML
     */
    @Test
    public void testStAXParse() {
        try {
            InputStream inputStream = DomTest.class.getClassLoader().getResourceAsStream(
                "xml/books.xml");
            XMLInputFactory xmlInputFactory = XMLInputFactory.newInstance();
            XMLStreamReader xmlStreamReader = xmlInputFactory.createXMLStreamReader(inputStream);
            while (xmlStreamReader.hasNext()) {
                int eventType = xmlStreamReader.next();
                // 如果是元素的开始
                if (eventType == XMLStreamConstants.START_ELEMENT) {
                    logger.info("localName:" + xmlStreamReader.getLocalName());
                    for (int i = 0; i < xmlStreamReader.getAttributeCount(); i++) {
                        logger.info("attribute name:" + xmlStreamReader.getAttributeName(i));
                        logger.info("attribute value:" + xmlStreamReader.getAttributeValue(i));
                    }
                }

                if (eventType == XMLStreamConstants.START_DOCUMENT) {
                    logger.info("start document");
                }
                if (eventType == XMLStreamConstants.END_DOCUMENT) {
                    logger.info("end document");
                }
                if (eventType == XMLStreamConstants.CHARACTERS) {
                    logger.info("text:" + xmlStreamReader.getText());
                }
            }
        } catch (Exception e) {
            logger.error("parse exception", e);
        }
    }
}
```

###### Java bean to XML
&#160; &#160; &#160; &#160;很多时候，我们希望解析过程自动化，毕竟上面的case代码看起来比较枯燥，又没有什么技术含量。开发人员，往往是面向业务开发，如果工具能直接从XML转换到Java Bean，从Java Bean转换到Xml，能大大降低开发成本。下面介绍的几个工具，都可以实现java bean和xml之间的互相转换。

- Digester
	
- JAXB
	
- XStream
示例代码：

```java
public class Author {
    /** */
    private String name;

    public Author(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}

public class AuthorConverter implements SingleValueConverter {

    public String toString(Object obj) {
        return ((Author) obj).getName();
    }

    public Object fromString(String name) {
        return new Author(name);
    }

    public boolean canConvert(Class type) {
        return type.equals(Author.class);
    }
}

public class Blog {
    private Author writer;
    private List   entries = new ArrayList();

    public Blog(Author writer) {
        this.writer = writer;
    }

    public void add(Entry entry) {
        entries.add(entry);
    }

    public List getContent() {
        return entries;
    }
}

public class Entry {
    /** */
    private String title;
    /** */
    private String description;

    /**
     * @param title
     * @param description
     */
    public Entry(String title, String description) {
        this.setTitle(title);
        this.setDescription(description);
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}

public class XstreamTest {
    /**
     *
     */
    @Test
    public void testToXml() {
        TestDolphin testDolphin = new TestDolphin();
        testDolphin.setName("andrew");
        XStream xStream = new XStream();
        xStream.alias("dolphin", TestDolphin.class);
        String xml = xStream.toXML(testDolphin);
        System.out.println("testDolphin:\n" + xml);

        TestDolphin newTestDolphin = (TestDolphin) xStream.fromXML(xml);
        Assert.assertEquals(newTestDolphin.isSmart(), testDolphin.isSmart());
    }

    @Test
    public void testToStarndXml() {
        Blog teamBlog = new Blog(new Author("Guilherme Silveira"));
        teamBlog.add(new Entry("first", "My first blog entry."));
        teamBlog.add(new Entry("tutorial",
            "Today we have developed a nice alias tutorial. Tell your friends! NOW!"));
        XStream xstream = new XStream();

        // class alias
        xstream.alias("blog", Blog.class);
        xstream.alias("entry", Entry.class);

        // field alias
        xstream.aliasField("author", Blog.class, "writer");

        // Implicit Collections
        xstream.addImplicitArray(Blog.class, "entries");

        // field as attribute
        xstream.useAttributeFor(Blog.class, "writer");
        xstream.registerConverter(new AuthorConverter());

        System.out.println("xml:");
        System.out.println(xstream.toXML(teamBlog));
    }
```

###### 对比Json,ProtoBuffer
- Json

- ProtoBuffer

###### 代码里
&#160; &#160; &#160; &#160;上面使用到的相关代码，参考GitHub上的[java-common](https://github.com/sunqinwpu/java-common)工程。


###### relative link
- [Document Object Model](https://en.wikipedia.org/wiki/Document_Object_Model)
- [Simple API for XML](https://en.wikipedia.org/wiki/Simple_API_for_XML)
- [Stax](https://zh.wikipedia.org/wiki/StAX)
- [ProtoBuffer](https://github.com/google/protobuf)
- [Json](https://zh.wikipedia.org/wiki/JSON)
- [Fastjson](https://github.com/google/protobuf)
