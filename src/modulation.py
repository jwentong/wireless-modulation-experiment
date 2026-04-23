"""
数字调制模块
实现BPSK、QPSK、16-QAM调制算法
"""

import numpy as np
from utils import plot_constellation


def bpsk_modulate(bits):
    """BPSK 调制"""
    # 映射规则：比特 0 -> +1，比特 1 -> -1
    symbols = 1 - 2 * bits
    return symbols.astype(complex)


def qpsk_modulate(bits):
    """QPSK 调制"""
    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")

    bits_reshaped = bits.reshape(-1, 2)
    symbols = np.zeros(len(bits_reshaped), dtype=complex)

    for i, (b0, b1) in enumerate(bits_reshaped):
        if b0 == 0 and b1 == 0:
            symbols[i] = 1 + 1j
        elif b0 == 0 and b1 == 1:
            symbols[i] = -1 + 1j
        elif b0 == 1 and b1 == 1:
            symbols[i] = -1 - 1j
        elif b0 == 1 and b1 == 0:
            symbols[i] = 1 - 1j

    # 功率归一化
    return symbols / np.sqrt(2)


def qam16_modulate(bits):
    """16-QAM 调制"""
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")

    bits_reshaped = bits.reshape(-1, 4)
    symbols = np.zeros(len(bits_reshaped), dtype=complex)

    # 格雷码映射字典
    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3
    }

    for i, (b0, b1, b2, b3) in enumerate(bits_reshaped):
        I = gray_map[(b0, b1)]
        Q = gray_map[(b2, b3)]
        symbols[i] = I + 1j * Q

    # 功率归一化，除以 √10
    return symbols / np.sqrt(10)


def test_modulation():
    """测试调制函数并生成星座图"""
    print("=" * 50)
    print("数字调制测试")
    print("=" * 50)

    # 测试BPSK
    print("\n1. 测试BPSK调制...")
    try:
        bits_bpsk = np.random.randint(0, 2, 1000)
        symbols_bpsk = bpsk_modulate(bits_bpsk)
        print(f"   输入比特数: {len(bits_bpsk)}")
        print(f"   输出符号数: {len(symbols_bpsk)}")
        print(f"   唯一符号: {np.unique(symbols_bpsk)}")
        plot_constellation(symbols_bpsk[:100], "BPSK星座图", "bpsk_constellation.png")
        print("   ✅ BPSK测试通过")
    except Exception as e:
        print(f"   ❌ BPSK测试失败: {e}")

    # 测试QPSK
    print("\n2. 测试QPSK调制...")
    try:
        bits_qpsk = np.random.randint(0, 2, 1000)
        symbols_qpsk = qpsk_modulate(bits_qpsk)
        print(f"   输入比特数: {len(bits_qpsk)}")
        print(f"   输出符号数: {len(symbols_qpsk)}")
        plot_constellation(symbols_qpsk[:200], "QPSK星座图", "qpsk_constellation.png")
        print("   ✅ QPSK测试通过")
    except Exception as e:
        print(f"   ❌ QPSK测试失败: {e}")

    # 测试16-QAM
    print("\n3. 测试16-QAM调制...")
    try:
        bits_qam = np.random.randint(0, 2, 1000)
        symbols_qam = qam16_modulate(bits_qam)
        print(f"   输入比特数: {len(bits_qam)}")
        print(f"   输出符号数: {len(symbols_qam)}")
        plot_constellation(symbols_qam[:250], "16-QAM星座图", "16qam_constellation.png")
        print("   ✅ 16-QAM测试通过")
    except Exception as e:
        print(f"   ❌ 16-QAM测试失败: {e}")

    print("\n" + "=" * 50)
    print("测试完成！请检查results/目录中的星座图。")
    print("=" * 50)

if __name__ == "__main__":
    test_modulation()