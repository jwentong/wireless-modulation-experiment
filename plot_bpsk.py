"""
绘制BPSK星座图
"""

import numpy as np
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.modulation import bpsk_modulate
from src.utils import plot_constellation

def plot_bpsk_constellation():
    """绘制BPSK星座图"""
    # 生成示例比特序列
    bits = np.array([0, 1])  # 两个点足够
    
    # 调制
    symbols = bpsk_modulate(bits)
    
    # 绘制星座图
    plot_constellation(symbols, "BPSK星座图", "bpsk_constellation.png")
    
    print("BPSK星座图已保存到 results/bpsk_constellation.png")

if __name__ == "__main__":
    plot_bpsk_constellation()