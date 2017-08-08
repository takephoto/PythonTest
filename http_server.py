# -*- coding:utf-8 -*-

import hashlib
import os

def _md5encode(encode_str):
    # 创建md5对象
    m = hashlib.md5()
    # 加密字符串
    m.update(encode_str)
    # 生成md5编码
    psw = m.hexdigest()
    assert isinstance(psw, object)
    return psw

print _md5encode('yang')
