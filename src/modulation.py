"""
数字调制模块
实现BPSK、QPSK、16-QAM调制算法
"""

import numpy as np
from utils import plot_constellation


def bpsk_modulate(bits):
    """BPSK调制：0 -> +1, 1 -> -1

    返回复数类型的符号数组并尝试保存星座图。
    """
    bits_arr = np.array(bits, dtype=int)
    if not np.all(np.isin(bits_arr, [0, 1])):
        raise ValueError("bits must be a binary sequence containing only 0 and 1")

    symbols = (1 - 2 * bits_arr).astype(np.complex128)

    try:
        plot_constellation(symbols[:200], "BPSK星座图", "bpsk_constellation.png")
    except Exception:
        pass

    return symbols


def qpsk_modulate(bits):
    """QPSK调制（格雷码）

    映射：
      00 -> (1+1j)/√2
      01 -> (-1+1j)/√2
      11 -> (-1-1j)/√2
      10 -> (1-1j)/√2
    """
    bits_arr = np.array(bits, dtype=int)
    if len(bits_arr) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")
    if not np.all(np.isin(bits_arr, [0, 1])):
        raise ValueError("bits must be a binary sequence containing only 0 and 1")

    pairs = bits_arr.reshape(-1, 2)
    norm = np.sqrt(2)
    mapping = {
        (0, 0): (1 + 1j) / norm,
        (0, 1): (-1 + 1j) / norm,
        (1, 1): (-1 - 1j) / norm,
        (1, 0): (1 - 1j) / norm,
    }

    symbols = np.array([mapping[tuple(p)] for p in pairs], dtype=np.complex128)

    try:
        plot_constellation(symbols[:200], "QPSK星座图", "qpsk_constellation.png")
    except Exception:
        pass

    return symbols


def qam16_modulate(bits):
    """16-QAM调制（格雷码，归一化至单位平均功率）"""
    bits_arr = np.array(bits, dtype=int)
    if len(bits_arr) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")
    if not np.all(np.isin(bits_arr, [0, 1])):
        raise ValueError("bits must be a binary sequence containing only 0 and 1")

    groups = bits_arr.reshape(-1, 4)
    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3,
    }

    norm = np.sqrt(10)
    symbols = []
    for g in groups:
        i_bits = (int(g[0]), int(g[1]))
        q_bits = (int(g[2]), int(g[3]))
        i_val = gray_map[i_bits]
        q_val = gray_map[q_bits]
        symbols.append((i_val + 1j * q_val) / norm)

    symbols = np.array(symbols, dtype=np.complex128)

    try:
        plot_constellation(symbols[:250], "16-QAM星座图", "16qam_constellation.png")
    except Exception:
        pass

    return symbols


def test_modulation():
    print("测试调制函数并生成星座图")
    bits = np.random.randint(0, 2, 1000)
    b = bpsk_modulate(bits)
    q = qpsk_modulate(bits[:(len(bits)//2)*2])
    m = qam16_modulate(bits[:(len(bits)//4)*4])
    print(len(b), len(q), len(m))


if __name__ == '__main__':
    test_modulation()
