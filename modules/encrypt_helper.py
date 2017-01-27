#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
class pyassetcrypt(object):
    def __init__(self):
        self.message = ""
    def encrypt_string(self, username, message):
        from Crypto.Cipher import AES, RSA
        import os.path
        IV = username
        checkfile = os.path.isfile(IV + ".pem") 
        if not checkfile:
            key = RSA.generate(4096)
            f = open(IV + '.pem','w')
            f.write(RSA.exportKey('PEM'))
            f.close()
        else:
            f = open(IV + '.pem','r')
            key = RSA.importKey(f.read())
        obj = AES.new(key, AES.MODE_CBC, IV)
        ciphertext = obj.encrypt(message)
        return ciphertext

    def decrypt_string(self, username, message):
        from Crypto.Cipher import AES, RSA
        import os.path
        IV = username
        checkfile = os.path.isfile(IV + ".pem") 
        if not checkfile:
            key = RSA.generate(4096)
            f = open(IV + '.pem','w')
            f.write(RSA.exportKey('PEM'))
            f.close()
        else:
            f = open(IV + '.pem','r')
            key = RSA.importKey(f.read())
        obj = AES.new(key, AES.MODE_CBC, IV)
        cleartext = obj.decrypt(message)
        return cleartext
