#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯手机端（iSH / 越狱环境）IPA / Mach-O 注入与打包简易脚本
用于在没有电脑的情况下，将 dylib 注入到 Mach-O 二进制文件中。
"""
import os
import sys
import struct
import subprocess

def print_help():
    print("=== 手机端轻量注入说明 ===")
    print("在越狱手机上（如 Dopamine 越狱环境），通常不需要修改 IPA 安装包。")
    print("直接编写 Theos Tweak 放入 /var/jb/Library/MobileSubstrate/DynamicLibraries/ 即可全局或针对 App 生效。")
    print("如果您确实需要修改 Mach-O 注入 Load Command，可以使用 optool 或 insert_dylib 核心逻辑。")

if __name__ == "__main__":
    print_help()
