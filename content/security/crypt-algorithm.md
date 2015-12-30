Title: 加密算法!
Date: 2015-06-02
Modified: 2015-06-02
Category: Security
Tags: 加密算法，摘要算法，对称加密，非对称加密
Slug: crypt-algorithms
Summary: 对常见的加密算法，实现、性能、安全性、应用场景做一个说明和对比

##### 我们可能面临的问题
- 如何存储网站用户名和密码，如何做登陆的时候，用户名和密码的校验?
- 如何加密你的文件，保证安全性?
- 如何防止网站被劫持？
- 如何确定，你访问的网站是真实的？

通过如下的加解密算法的说明，希望能间接地地回答这些问题。


##### 消息摘要算法
消息摘要算法包括MD(Message Digest 消息摘要算法)，SHA(Secure Hash Algorithm 安全散列算法)和MAC(Message authentication code消息验证码)三个系列。主要用于验证数据的完整性，密码加密等领域。
###### MD系列算法 
MD系列算法包括MD,MD2,MD3,MD4,MD5。是一个不断优化改进的过程。MD5是输入不定长信息，输出固定长度128-bits的算法。基本方式为，求余、取余、调整长度、与链接变量进行循环运算。经过程序流程，生成四个32位数据，最后联合起来成为一个128-bits散列。
- 性能
- 安全性。
	- MD5会产生Hash碰撞，不适用于SSL证书，数字签章。
    - 彩虹表反查，可以轻松破解。加salt之后，会乐观点，取决于salt的长度。某些网站，轻松使用大数据，上百TB的硬盘，存储了大量组合的MD5值。
    
最好不要在密码校验的场景使用MD5。目前只适合校验数据完整性。

###### SHA系列算法
SHA系列包括五个算法，分别是SHA-1、SHA-224、SHA-256、SHA-384，和SHA-512,后4中并称为SHA2。
SHA是FIPS所认证的五种安全散列算法。这些算法之所以称作“安全”是基于以下两点（根据官方标准的描述）：
- 由消息摘要反推原输入消息，从计算理论上来说是很困难的。
- 想要找到两组不同的消息对应到相同的消息摘要，从计算理论上来说也是很困难的。任何对输入消息的变动，都有很高的概率导致其产生的消息摘要迥异。
SHA-1应用在很多安全领域，曾被视为MD5的后继者，不过现在安全性受到严重质疑。目前为止尚无对SHA2的有效攻击，不过SHA2的算法和HSA1基本相似。

###### MAC
MAC与MD和SHA不同，MAC是含有密钥的散列函数算法，我们也常把MAC称为HMAC。 

###### 慢Hash函数
一般网站在存储用户密码的时候，使用上述的散列算法进行散列后存储，在用户登录的时候，对用户输入的密码做散列，然后对比验证。如果网站密码泄露，被黑客获取，通过彩虹表可以轻松破解。为了应对破解的问题，有了3种新的慢Hash函数，所谓慢Hash，就是让签名的过程变得很慢，需要消耗更多地cpu和内存，使黑客建立彩虹表的成本变高。目前主要有三种bcrypt,scrypt,PBKDF2。
- PBKDF2(Password-Based Key Derivation Function)。PBKDF2简单而言就是将salted hash进行多次重复计算，这个次数是可选择的。如果计算一次所需要的时间是1微秒，那么计算1百万次就需要1秒钟。假如攻击一个密码所需的rainbow table有1千万条，建立所对应的rainbow table所需要的时间就是115天。这个代价足以让大部分的攻击者忘而生畏。
- bcrypt。bcrypt是专门为密码存储而设计的算法，基于Blowfish加密算法变形而来，由Niels Provos和David Mazières发表于1999年的USENIX。
bcrypt最大的好处是有一个参数（work factor)，可用于调整计算强度，而且work factor是包括在输出的摘要中的。随着攻击者计算能力的提高，使用者可以逐步增大work factor，而且不会影响已有用户的登陆。
bcrypt经过了很多安全专家的仔细分析，使用在以安全著称的OpenBSD中，一般认为它比PBKDF2更能承受随着计算能力加强而带来的风险。bcrypt也有广泛的函数库支持，因此使用这种方式存储密码会更安全。
- scrypt。scrypt是由著名的FreeBSD黑客 Colin Percival为他的备份服务 Tarsnap开发的。
和上述两种方案不同，scrypt不仅计算所需时间长，而且占用的内存也多，使得并行计算多个摘要异常困难，因此利用rainbow table进行暴力攻击更加困难。scrypt没有在生产环境中大规模应用，并且缺乏仔细的审察和广泛的函数库支持。但是，scrypt在算法层面只要没有破绽，它的安全性应该高于PBKDF2和bcrypt。
涉及的问题: MD5,SHA-1,HMAC,bcrypt,scrypt,PBKDF2

##### 对称加密算法:
涉及的问题: DES,3DES,Blowfish,IDEA,RC4,RC5,RC6,AES


- ECB/CBC/CFB/OFB/CTR

##### 非对称加密算法:
涉及的问题:公钥,私钥,证书系统,RSA,ECC,E1 Gamal,DSA,Diffie–Hellman key exchange。

Base64编码


RSA/ECB/PKCS1Padding

相关链接
- [HMAC](http://en.wikipedia.org/wiki/Hash-based_message_authentication_code)
- [PBKDF2](http://en.wikipedia.org/wiki/PBKDF2)
- [Let's Encrypt](https://letsencrypt.org/)
- [Java C# AES ](https://zenu.wordpress.com/2011/09/21/aes-128bit-cross-platform-java-and-c-encryption-compatibility/)
