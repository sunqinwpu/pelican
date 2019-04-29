Title: GPG(Gnu Privacy Guird) & GnuPG
Date: 2015-11-30
Modified: 2015-11-30
Category: Technology
Tags: GPG,encrypt,email
Slug: gnu-privacy-guird
Summary: Gnu Privacy Guird

###### 概述
如何进行可靠的安全通信,从古至今一直就是一个问题。本文所说的可靠安全，不是说信息可到达性。本文所说包括2个维度：
- 隐私性。即如何保障只有通信双方知道通信的内容，而不被其他人获知。
- 完整性。即如何验证，信息确实是由正确的发送者发出，而不是被其他人伪造的，或者是被其他人篡改过。

接下来，介绍一种对电子邮件进行加密的通信方式，该方式可以保证通信的隐私和完整。学习下面的文章之前，建议先熟悉下[非对称加密](https://zh.wikipedia.org/wiki/%E5%85%AC%E5%BC%80%E5%AF%86%E9%92%A5%E5%8A%A0%E5%AF%86),[RSA加密算法](https://zh.wikipedia.org/wiki/RSA%E5%8A%A0%E5%AF%86%E6%BC%94%E7%AE%97%E6%B3%95)

###### 加密通信的原理
保证安全通信包括2个部分，加密和数字签名，这2部分略有不同。首先为了开始通信，通信参与者需要生成密钥对，公钥开放出去，私钥自己保留。
- 加密。如果A需要对B发送信息，则A使用B的公钥对信息进行加密，B收到信息后进行解密。这个过程中，其他人即使收到A发送给B的信息，因为没有B的私钥，无法进行解密。
- 签名。如上，A对B发送信息的时候，不仅使用B的公钥进行加密，同时使用自己的私钥对加密后的信息进行签名。当B收到信息后，可以使用A的公钥对签名进行校验。在这个过程中，验证了消息来源于A，其他人没有A的私钥，无法冒充A对信息进行签名。

上面的方法过程中，涉及到了加密解密，数字签名的过程，还需要对秘钥进行管理。为了使用上面的方法，需要高效的工具来完成。

###### PGP/GnuPG
[PGP (Pretty Good Privacy)](http://archboy.org/2013/04/18/gnupg-pgp-encrypt-decrypt-message-and-email-and-digital-signing-easy-tutorial/%EF%BC%88http://en.wikipedia.org/wiki/Pretty_Good_Privacy%EF%BC%89) 是由 [Phil Zimmermann](https://en.wikipedia.org/wiki/Phil_Zimmermann) 于 1991 开发的一个用于数据加密和数字签名的程序，由于被广泛应用以至于后来形成一个开放的标准 [OpenPGP](www.openpgp.org)，而 [GnuPG](www.gnupg.org) 则是实现了该标准的一个开源免费程序，本文将会简单介绍如何使用 GnuPG 管理钥匙、加密解密文件和电子邮件、数字签名文件和电子邮件等内容。
###### GnuPg安装
Linux系统基本都自带了GnuPG套件，直接通过软件源安装即可。Mac系统，可以在[https://gpgtools.org/](https://gpgtools.org/)下载，工具可以和Mac自带Mail客户端配合使用。
###### 秘钥管理
以下介绍下gnupg的一些命令。
1. 生成秘钥
<pre><code>gpg --gen-key</code></pre>
该命令会产生一对全球唯一的公私钥对。接下来会让你填写加密算法，秘钥长度，过期时间。如何填写，需要先了解非对称加密算法。
接下来会有三个个人信息需要填写。
<pre><code>
Real name: dolphin
Email address: dolphin@126.com
Comment: dolphin on Twitter
</code></pre>
这三行信息用于产生一个标识（uid），用来标识这个钥匙对。名字或者email地址来指定这个钥匙对。
因为 GnuPG 的钥匙（包括公钥和私钥）是保存在本机上的，如果有人或者黑客进入你的计算机把你的私钥盗走了，那么你的身份就有被冒充的危险。所以接下来你需要输入一个密码用于保护你的私钥。这个密码最好选择一个稍微复杂一些的。
接下来就默默等待程序生成公私钥了，这个过程可能会有点长，几分钟左右，可以喝杯茶，休息一下。
2. 查看秘钥
使用下面的命令，可以列出所有的密钥。
<pre><code>gpg --list-keys</code></pre>
<pre><code>
pub   4096R/4A987CF6 2015-02-13 [expires: 2019-02-13]
uid       [ultimate] sunqi <sunqinwpu@gmail.com>
uid       [ultimate] [jpeg image of size 435418]
sub   4096R/01D657D9 2015-02-13 [expires: 2019-02-13]
</code></pre>
上面是我gmail邮箱，生成的秘钥。这里会包括所有的公钥，你自己的和你导入的别人的。
而使用
<pre><code>gpg --list-secret-keys</code></pre>
可以列出所有的私钥。
3. 导出公钥
为了把公钥分享给别人，需要把公钥导出为1个文件。
<pre><code>gpg -a --output key.public --export sunqinwpu@gmail.com</code></pre>
可以把公钥导出。我的公钥，见链接[sunqinwpu@gmail.com](https://libereco.cn/sunqinwpu@gmail.gpg)。欢迎大家给我发加密邮件~~。
4. 发布公钥到公钥服务器
公钥服务器用于储存和发布用户的公钥以便相互交流，这些服务都是免费的，GnuPG 默认的公钥服务器是 keys.gnupg.net，你可以在这里找到更多的服务器。你也可以使用浏览器打开它们的网站，然后把你的公钥复制粘贴上去。当然最直接的是通过命令行：
<pre><code>gpg --keyserver keys.gnupg.net --send-keys 4A987CF6</code></pre>
5. 导入公钥
为了和别人通信，需要导入公钥。导入公钥的命令。导入公钥有两种方式，一种是在公钥服务器搜索到用户的公钥，通过公钥服务器导入，另一种是直接导入公钥文件。
6. 核对公钥指纹并签收
把公钥导入本机后，就可以使用公钥进行加密通信了。不过每次，都会提示公钥不可信。虽然你导入了公钥，但是公钥可能是别人冒用发布的，你需要验证公钥的指纹，确认公钥，并签收。
<pre><code>gpg --fingerprint
pub   4096R/4A987CF6 2015-02-13 [expires: 2019-02-13]
      Key fingerprint = 200D 8D17 ECA3 B8ED 7A5B  354C 8C7D 770A 4A98 7CF6
uid       [ultimate] sunqi <sunqinwpu@gmail.com>
uid       [ultimate] [jpeg image of size 435418]
sub   4096R/01D657D9 2015-02-13 [expires: 2019-02-13]
</code></pre>
这里列出了公钥的指纹。你应该通过某种可信任的方式，确认公钥的指纹和公钥是一致的，比如打电话、当面验证等等。验证ok后，使用如下命令进行签收。
<pre><code>gpg --sign-key sunqinwpu@126.com</code></pre>

###### 邮件加密及签名
对于Mac，安装完套件后。就可以使用Mail通信了。
![Alt text](https://libereco.cn/pictures/5296c5062412f590f09bec481ccadf56.png)
上图的小锁代表加密，小锁右面的标签代表签名。
###### 可靠通信扩展
以前只是谈及邮件安全，但在今天的通信中，我们使用邮件越来越少，使用即时通信软件越来越多。微信，微博，whatsapp等待。关于使用即时通信软件通信的安全性如何呢？

这是另一个话题。待我深入研究下，再带来另一篇分析。

###### 相关链接
- [https://www.gnupg.org](https://www.gnupg.org)
- [https://gpgtools.org/](https://gpgtools.org/)
- [GPGTools on Github](https://github.com/GPGTools/MacGPG2)
