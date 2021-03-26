'''
实现加密、解密，签名、验签，生成密钥的文件
'''
import base64

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

import hashlib

public_key_native = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt1MZbsEOGIli2cGEGOO3
VHv+O0s41ex8KQMECw0x2B9rAXwyMfjNbAnH+TakMF2tEjGcfj/qWiOY9MQrRCe8
hfz+2R9kRcimZoT7DCFbHcTLu4ADpWiwBjisZgB7j8QlkXwRmaMNdTUyzJVRgFAh
1y/Q14fGWNQ9o1foooT6YDU/hTObyINETtL09luZVEGWWiNEAa08w3lpe+5STeBL
r81+PB0+u0OpcxUxAwqIx/rxhuZNVkuoguUywEJhiYZ8e6qR1NGL5POolsoQMY8X
EIVik9fqPrEgkpHRTZib7CUfMevaOVaW+nYuBO/PK1376ePO4QhGsX4OrFab/NzO
CwIDAQAB
-----END PUBLIC KEY-----'''

def encrypt_data(msg):
    """
    公钥加密
    :param msg: 要加密内容
    :return:  加密之后的密文
    """
    publickey = RSA.importKey(public_key_native)
    # 分段加密
    pk = PKCS1_cipher.new(publickey)
    encrypt_text = []
    for i in range(0,len(msg),100):
        cont = msg[i:i+100]
        encrypt_text.append(pk.encrypt(cont.encode()))
    # 加密完进行拼接
    cipher_text = b''.join(encrypt_text)
    result = base64.b64encode(cipher_text)
    return result.decode()


def decrypt_data(msg, privatekey):
    """
    私钥进行解密
    :param msg: 密文：字符串类型
    :return:  解密之后的内容
    """
    msg = base64.b64decode(msg)
    rsakey = RSA.importKey(privatekey)
    cipher =  PKCS1_cipher.new(rsakey)
    text = []
    #2048bit密钥256，1024bit密钥128
    for i in range(0,len(msg),256):
        cont = msg[i:i+256]
        text.append(cipher.decrypt(cont,1))
    text = b''.join(text)
    return text.decode()

def sha_data(msg):
    s = hashlib.sha256()
    s.update(msg.encode("utf-8"))
    return(s.hexdigest())

def rsa_sinature_encode(message, private_key):
    rsakey = RSA.importKey(private_key)
    signer = PKCS1_signature.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    return signature

def rsa_signature_decode(message, signature):
    rsakey = RSA.importKey(public_key_native)
    signer = PKCS1_signature.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf8"))
    is_verify = signer.verify(digest, base64.b64decode(signature))
    return is_verify

def creat_pem():
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    # 生成私钥
    private_key = rsa.exportKey()
    print(private_key.decode('utf-8'))
    # 生成公钥
    public_key = rsa.publickey().exportKey()
    print(public_key.decode('utf-8'))

    with open('rsa_private_key.pem', 'wb')as f:
        f.write(private_key)
        
    with open('rsa_public_key.pem', 'wb')as f:
        f.write(public_key)