#!usr/bin/python3
# _*_ coding: utf-8 _*_
import hashlib

s = '1234567890123456789012345678901234'
h1 = hashlib.md5()
h1.update(s.encode(encoding='utf-8'))
print(s, h1.hexdigest(), len(h1.hexdigest()))
