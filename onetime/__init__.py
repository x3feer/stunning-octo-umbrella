#!/usr/bin/python3

import random
import hashlib
import hmac
import time
import base64

def SecretGenerate(lenght=16):

    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for Number in range(lenght))

def SecretPattern(Secret):

    Secret = str(Secret)

    if len(Secret) % 8:

        Secret += '=' * (8 - len(Secret) % 8)

    return base64.b32decode(Secret)

def TimePattern(Time):

    Time = int(Time)
    Pattern = bytearray()

    while Time != 0:
        Pattern.append(Time & 0xFF)
        Time >>= 8

    return bytes(bytearray(reversed(Pattern)).rjust(8, b'\0'))

def GenerateOTP(Secret):

    Time = time.time() // 30
    Hash = hmac.new(SecretPattern(Secret), TimePattern(Time), hashlib.sha1)
    Hash = bytearray(Hash.digest())

    Offset = Hash[-1] & 0xf
    Coding = ((Hash[Offset] & 0x7f) << 24 | (Hash[Offset + 1] & 0xff) << 16 | (Hash[Offset + 2] & 0xff) << 8 | (Hash[Offset + 3] & 0xff))
    Coding = str(Coding % 10 ** 6)

    while len(Coding) < 6:
        Coding = '0' + Coding

    return Coding

def CheckCode(Secret, Coding):

    return GenerateOTP(Secret) == Coding

print(SecretGenerate())
