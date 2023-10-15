#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 引数で指定され与えられたファイルをバイナリーとして読み取り構造体として定義したデータとして表示する
# バイナリファイルはリトルエンディアンの以下の構造体で定義されているものとする
#
# #pragma pack(1)
# struct A {
# 	char a;
# 	uint32_t b;
# };
# define SIZE 4
# struct B {
# 	char c;
# 	struct A d;
# 	struct A e[SIZE];
#	uint8_t f[SIZE];
# };


import sys
import struct
import os.path
import ctypes

# バイナリーファイルを読み込む
def read_binary_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

# self-descriptive structure
class DescriptiveStruct(ctypes.LittleEndianStructure):
    _indent = 0
    _pack_ = 1
    def describe(self):
        print("{")
        DescriptiveStruct._indent += 1
        for field_name, field_type in self._fields_:
            if issubclass(field_type, ctypes.Array):
                self.indent_print(f"{field_name}=[")
                DescriptiveStruct._indent += 1
                for i in range(len(getattr(self, field_name))):
                    self.indent_print(f"[{i}]=", end="")
                    val = getattr(self, field_name)[i]
                    if issubclass(type(val), DescriptiveStruct):
                        val.describe()
                    else:
                        print(val)
                DescriptiveStruct._indent -= 1
                self.indent_print("]")
            elif issubclass(field_type, DescriptiveStruct):
                self.indent_print(f"{field_name}=", end="")
                getattr(self, field_name).describe()                
            else:
                self.indent_print(f"{field_name}={getattr(self, field_name)}")
        DescriptiveStruct._indent -= 1
        self.indent_print("}")

    def indent_print(self, *args, **kwargs):
        print('  ' * DescriptiveStruct._indent, end='')
        print(*args, **kwargs)


# 表示する構造体を定義
class A(DescriptiveStruct):
    _fields_ = [
        ('a', ctypes.c_uint8),
        ('b', ctypes.c_uint32)
    ]

class B(DescriptiveStruct):
    _fields_ = [
        ('c', ctypes.c_char),
        ('d', A),
        ('e', A * 4),
        ('f', ctypes.c_uint8 * 4)
    ]
    
# バイナリーファイルを読み込みBとして表示する
def dump_binary_file(filename):
    data = read_binary_file(filename)
    mystruct = B.from_buffer_copy(data)
    mystruct.describe()


# メインルーチン
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {os.path.basename(sys.argv[0])} filename")
        sys.exit(1)
    dump_binary_file(sys.argv[1])


    
    


    
