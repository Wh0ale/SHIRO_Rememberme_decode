# SHIRO_Rememberme_decode
[Apache Shiro payload AES解密](https://www.t00ls.net/thread-56799-1-1.html)

**恶意 Cookie rememberMe值构造**

前16字节的密钥 -> 后面加入序列化参数 -> AES加密 -> base64编码 -> 发送cookie

**Apache Shiro处理cookie的流程**

得到rememberMe的cookie值 -> Base64解码 -> AES-128-CBC解密-> 反序列化(readobject)。

rememberMe管理器代码中写到cookie加密密钥默认为AES算法，可以将黑客常用的攻击密钥做一个keylist进行解密

效果
![1](https://user-images.githubusercontent.com/44937351/110765107-cc54ab80-828e-11eb-9bef-7218fbc9ddfc.png)
![2](https://user-images.githubusercontent.com/44937351/110765116-ceb70580-828e-11eb-838b-a51682cc6006.png)


通过以下解密可以查看到攻击者开启JRMP Server的vps还有使用的dns平台（ceye,dnslog,burp等），和攻击日志里的host进行关联，发现攻击者所拥有的基础设施，通过奇技淫巧挖掘出更多攻击者的信息。顺着网线给攻击者查水表。

这里只是举个发现攻击者的小例子，欢迎师傅多多交流。

参考：

https://www.anquanke.com/post/id/193165
