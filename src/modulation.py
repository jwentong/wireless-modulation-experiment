"""
数字调制模块
实现BPSK、QPSK、16-QAM调制算法
"""

import numpy as np

from utils import plot_constellation


def bpsk_modulate(bits):
    """
    BPSK (Binary Phase Shift Keying) 调制

    任务要求：
    - 输入：二进制比特序列（NumPy数组），元素为0或1
    - 输出：调制后的复数符号序列
    - 映射规则：
        比特 0 → 符号 +1
        比特 1 → 符号 -1

    参数:
        bits: 二进制比特数组，例如 np.array([0, 1, 0, 1, 1, 0])

    返回:
        symbols: 复数符号数组，例如 np.array([1, -1, 1, -1, -1, 1])
    """
    bits = np.asarray(bits, dtype=int)
    return (1 - 2 * bits).astype(np.complex128)


def qpsk_modulate(bits):
    """
    QPSK (Quadrature Phase Shift Keying) 调制

    任务要求：
    - 输入：二进制比特序列（长度必须是2的倍数）
    - 输出：调制后的复数符号序列
    - 每2个比特映射到1个符号（格雷码映射）：
        00 → (1+1j)/√2
        01 → (-1+1j)/√2
        11 → (-1-1j)/√2
        10 → (1-1j)/√2

    参数:
        bits: 二进制比特数组，长度必须是偶数

    返回:
        symbols: 复数符号数组，长度是bits的一半
    """
    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")

    bit_pairs = np.asarray(bits, dtype=int).reshape(-1, 2)
    mapping = {
        (0, 0): 1 + 1j,
        (0, 1): -1 + 1j,
        (1, 1): -1 - 1j,
        (1, 0): 1 - 1j,
    }
    symbols = np.array([mapping[tuple(pair)] for pair in bit_pairs], dtype=np.complex128)
    return symbols / np.sqrt(2)


def qam16_modulate(bits):
    """
    16-QAM (16-Quadrature Amplitude Modulation) 调制

    任务要求：
    - 输入：二进制比特序列（长度必须是4的倍数）
    - 输出：调制后的复数符号序列
    - 每4个比特映射到1个符号
    - I路和Q路分量取值：{-3, -1, +1, +3}

    参数:
        bits: 二进制比特数组，长度必须是4的倍数

    返回:
        symbols: 复数符号数组，长度是bits的四分之一
    """
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")

    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3,
    }
    bit_groups = np.asarray(bits, dtype=int).reshape(-1, 4)
    i_components = np.array([gray_map[tuple(group[:2])] for group in bit_groups], dtype=float)
    q_components = np.array([gray_map[tuple(group[2:])] for group in bit_groups], dtype=float)
    return (i_components + 1j * q_components) / np.sqrt(10)


def test_modulation():
    """测试调制函数并生成星座图。"""
    print("=" * 50)
    print("数字调制测试")
    print("=" * 50)

    bits_bpsk = np.random.randint(0, 2, 1000)
    symbols_bpsk = bpsk_modulate(bits_bpsk)
    print("\n1. 测试BPSK调制...")
    print(f"   输入比特数: {len(bits_bpsk)}")
    print(f"   输出符号数: {len(symbols_bpsk)}")
    print(f"   唯一符号: {np.unique(symbols_bpsk)}")
    plot_constellation(symbols_bpsk[:100], "BPSK星座图", "bpsk_constellation.png")
    print("   ✅ BPSK测试通过")

    bits_qpsk = np.random.randint(0, 2, 1000)
    symbols_qpsk = qpsk_modulate(bits_qpsk)
    print("\n2. 测试QPSK调制...")
    print(f"   输入比特数: {len(bits_qpsk)}")
    print(f"   输出符号数: {len(symbols_qpsk)}")
    print(f"   符号幅度: {np.abs(symbols_qpsk[:4])}")
    plot_constellation(symbols_qpsk[:200], "QPSK星座图", "qpsk_constellation.png")
    print("   ✅ QPSK测试通过")

    bits_qam = np.random.randint(0, 2, 1000)
    symbols_qam = qam16_modulate(bits_qam)
    print("\n3. 测试16-QAM调制...")
    print(f"   输入比特数: {len(bits_qam)}")
    print(f"   输出符号数: {len(symbols_qam)}")
    print(f"   唯一符号数量: {len(np.unique(symbols_qam))}")
    plot_constellation(symbols_qam[:250], "16-QAM星座图", "16qam_constellation.png")
    print("   ✅ 16-QAM测试通过")

    print("\n" + "=" * 50)
    print("测试完成！请检查results/目录中的星座图。")
    print("=" * 50)


if __name__ == "__main__":
    test_modulation()
