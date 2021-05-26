# coding=utf-8
import configparser
import fcntl
import os
from ctypes import cdll, POINTER, c_uint, create_string_buffer, byref


def get_conf(section, key, path):
    conf = configparser.ConfigParser()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            conf.read_file(f)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        str_val = conf.get(section, key)
    except Exception:
        str_val = None
    return str_val


class SecpspApi:
    def __init__(self, so_path, moid):
        self.kdvsecpspapi = cdll.LoadLibrary(so_path)
        self.protect_key = self.get_protect_key(moid)

    # KdvSecPspGenProtectKey
    def get_protect_key(self, moid):
        pFator1 = create_string_buffer(
            moid.encode('utf-8'))              # 生成因子1，写死在代码中的一个随机数；
        uFactor1Len = c_uint(len(moid))        # 因子1长度；
        pFator2 = POINTER(c_uint)()            # 生成因子2，设备的唯一ID，HEX编码；
        uFactor2Len = c_uint(0)                # 因子2长度；
        pKey = create_string_buffer(64)        # 保护密钥，HEX编码；
        puLen = c_uint(64)                     # 保护密钥缓冲区长度。
        self.kdvsecpspapi.KdvSecPspGenProtectKey(
            byref(pFator1),
            uFactor1Len,
            pFator2,
            uFactor2Len,
            byref(pKey),
            byref(puLen))
        return pKey.raw

    def decrypt_data(self, data, cipheralgo=b'SM4'):
        data = bytes.fromhex(data)
        cipheralgo = create_string_buffer(cipheralgo)         # 对称加密算法类型；
        pKey = create_string_buffer(self.protect_key)         # 保护密钥；
        uKeyLen = c_uint(len(self.protect_key))               # 保护密钥长度；
        pEncData = create_string_buffer(data)                 # 数据密文，十六进制数据；
        uEncDataLen = c_uint(len(data))                       # 数据密文长度；
        pDecData = create_string_buffer(64)                   # 数据原文，十六进制数据；
        puDecDataLen = c_uint(64)                             # 原文缓冲区长度。
        self.kdvsecpspapi.KdvSecPspDecryptData(
            byref(cipheralgo),
            byref(pKey),
            uKeyLen,
            byref(pEncData),
            uEncDataLen,
            byref(pDecData),
            byref(puDecDataLen))
        return pDecData.value.decode('utf-8')
