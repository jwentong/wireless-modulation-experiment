"""数字调制模块：实现 BPSK、QPSK、16-QAM 调制算法。"""

import numpy as np
from utils import plot_constellation


def bpsk_modulate(bits):
    """
    BPSK 调制。

    映射关系：
    0 -> +1
    1 -> -1
    """
    bits = np.asarray(bits, dtype=int)

    if not np.all((bits == 0) | (bits == 1)):
        raise ValueError("BPSK 输入比特只能包含 0 或 1")

    symbols = 1 - 2 * bits
    return symbols.astype(complex)


def qpsk_modulate(bits):
    """
    QPSK 调制，采用格雷码映射。

    00 -> ( 1 + 1j) / sqrt(2)
    01 -> (-1 + 1j) / sqrt(2)
    11 -> (-1 - 1j) / sqrt(2)
    10 -> ( 1 - 1j) / sqrt(2)
    """
    bits = np.asarray(bits, dtype=int)

    if not np.all((bits == 0) | (bits == 1)):
        raise ValueError("QPSK 输入比特只能包含 0 或 1")

    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")

    bit_pairs = bits.reshape(-1, 2)
    mapping = {
        (0, 0): (1 + 1j) / np.sqrt(2),
        (0, 1): (-1 + 1j) / np.sqrt(2),
        (1, 1): (-1 - 1j) / np.sqrt(2),
        (1, 0): (1 - 1j) / np.sqrt(2),
    }

    symbols = np.array([mapping[tuple(pair)] for pair in bit_pairs], dtype=complex)
    return symbols


def qam16_modulate(bits):
    """
    16-QAM 调制，采用格雷码映射。

    每 4 个比特映射成 1 个复数符号：
    前 2 位决定 I 路，后 2 位决定 Q 路。

    00 -> +3
    01 -> +1
    11 -> -1
    10 -> -3

    归一化因子 sqrt(10)，使平均符号功率约为 1。
    """
    bits = np.asarray(bits, dtype=int)

    if not np.all((bits == 0) | (bits == 1)):
        raise ValueError("16-QAM 输入比特只能包含 0 或 1")

    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")

    bit_groups = bits.reshape(-1, 4)

    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3,
    }

    symbols = []
    for group in bit_groups:
        i_bits = tuple(group[:2])
        q_bits = tuple(group[2:])
        i_value = gray_map[i_bits]
        q_value = gray_map[q_bits]
        symbols.append((i_value + 1j * q_value) / np.sqrt(10))

    return np.array(symbols, dtype=complex)


def test_modulation():
    """测试调制函数并生成星座图。"""
    print("=" * 50)
    print("数字调制测试")
    print("=" * 50)

    print("\n1. 测试BPSK调制...")
    bits_bpsk = np.random.randint(0, 2, 1000)
    symbols_bpsk = bpsk_modulate(bits_bpsk)
    print(f"输入比特数: {len(bits_bpsk)}")
    print(f"输出符号数: {len(symbols_bpsk)}")
    print(f"唯一符号: {np.unique(symbols_bpsk)}")
    plot_constellation(symbols_bpsk[:100], "BPSK星座图", "bpsk_constellation.png")
    print("✅ BPSK测试通过")

    print("\n2. 测试QPSK调制...")
    bits_qpsk = np.random.randint(0, 2, 1000)
    symbols_qpsk = qpsk_modulate(bits_qpsk)
    print(f"输入比特数: {len(bits_qpsk)}")
    print(f"输出符号数: {len(symbols_qpsk)}")
    print(f"符号幅度: {np.abs(symbols_qpsk[:4])}")
    plot_constellation(symbols_qpsk[:200], "QPSK星座图", "qpsk_constellation.png")
    print("✅ QPSK测试通过")

    print("\n3. 测试16-QAM调制...")
    bits_qam = np.random.randint(0, 2, 1000)
    symbols_qam = qam16_modulate(bits_qam)
    print(f"输入比特数: {len(bits_qam)}")
    print(f"输出符号数: {len(symbols_qam)}")
    print(f"唯一符号数量: {len(np.unique(np.round(symbols_qam, 4)))}")
    plot_constellation(symbols_qam[:250], "16-QAM星座图", "16qam_constellation.png")
    print("✅ 16-QAM测试通过")

    print("\n" + "=" * 50)
    print("测试完成！请检查 results/ 目录中的星座图。")
    print("=" * 50)


if __name__ == "__main__":
    test_modulation()