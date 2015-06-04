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
SHA系列包括五个算法，分别是SHA-1、SHA-224、SHA-256、SHA-384，和SHA-512。SHA-1应用在很多安全领域，曾被视为MD5的后继者，不过现在安全性受到严重质疑。

###### MAC

###### 慢Hash函数
涉及的问题: MD5,SHA-1,HMAC,bcrypt,scrypt,PBKDF2

对称加密算法:
涉及的问题: DES,3DES,Blowfish,IDEA,RC4,RC5,RC6,AES

非对称加密算法:
涉及的问题:公钥,私钥,证书系统,RSA,ECC,E1 Gamal,DSA,Diffie–Hellman key exchange。





相关链接
- [HMAC](http://en.wikipedia.org/wiki/Hash-based_message_authentication_code)
- [PBKDF2](http://en.wikipedia.org/wiki/PBKDF2)
- [Let's Encrypt](https://letsencrypt.org/)
