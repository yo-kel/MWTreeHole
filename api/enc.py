import base64

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

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
    public_key = RSA.importKey(public_key_native)
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')

def decrypt_data(encrypt_msg,private_key_native):
    private_key = RSA.importKey(private_key_native)
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
    return back_text.decode('utf-8')

def rsa_sinature_encode(message, private_key):
    rsakey = RSA.importKey(private_key)
    signer = signature_PKCS1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    return signature

def rsa_signature_decode(message, signature):
    rsakey = RSA.importKey(public_key_native)
    signer = signature_PKCS1_v1_5.new(rsakey)
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