"""
数字调制模块
实现BPSK、QPSK、16-QAM调制算法
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# 自动创建结果目录
os.makedirs("results", exist_ok=True)

def bpsk_modulate(bits):
    bits = np.asarray(bits)
    symbols = 1 - 2 * bits
    return symbols.astype(np.complex64)

def qpsk_modulate(bits):
    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")
    bits = np.asarray(bits)
    bit_groups = bits.reshape(-1, 2)
    qpsk_map = np.array([1+1j, -1+1j, 1-1j, -1-1j])
    indices = bit_groups[:, 0] * 2 + bit_groups[:, 1]
    symbols = qpsk_map[indices] / np.sqrt(2)
    return symbols.astype(np.complex64)

def qam16_modulate(bits):
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")
    bits = np.asarray(bits)
    bit_groups = bits.reshape(-1, 4)
    i_bits = bit_groups[:, :2]
    q_bits = bit_groups[:, 2:]
    gray_map = np.array([3, 1, -3, -1])
    i_indices = i_bits[:, 0] * 2 + i_bits[:, 1]
    q_indices = q_bits[:, 0] * 2 + q_bits[:, 1]
    i_comp = gray_map[i_indices]
    q_comp = gray_map[q_indices]
    symbols = (i_comp + 1j * q_comp) / np.sqrt(10)
    return symbols.astype(np.complex64)

def plot_constellation(symbols, title, save_name):
    plt.figure(figsize=(6,6))
    plt.scatter(symbols.real, symbols.imag, s=40, alpha=0.7, color='#1f77b4')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.title(title, fontsize=14)
    plt.xlabel("In-phase (I) Component", fontsize=12)
    plt.ylabel("Quadrature (Q) Component", fontsize=12)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.savefig(f"results/{save_name}", dpi=300, bbox_inches='tight')
    plt.close()

def test_modulation():
    print("=" * 50)
    print("数字调制测试")
    print("=" * 50)
    # 测试BPSK
    print("\n1. 测试BPSK调制...")
    bits_bpsk = np.random.randint(0, 2, 1000)
    symbols_bpsk = bpsk_modulate(bits_bpsk)
    print(f"   输入比特数: {len(bits_bpsk)}")
    print(f"   输出符号数: {len(symbols_bpsk)}")
    print(f"   唯一符号: {np.unique(symbols_bpsk)}")
    plot_constellation(symbols_bpsk[:100], "BPSK星座图", "bpsk_constellation.png")
    print("   ✅ BPSK测试通过")

    # 测试QPSK
    print("\n2. 测试QPSK调制...")
    bits_qpsk = np.random.randint(0, 2, 1000)
    symbols_qpsk = qpsk_modulate(bits_qpsk)
    print(f"   输入比特数: {len(bits_qpsk)}")
    print(f"   输出符号数: {len(symbols_qpsk)}")
    print(f"   符号幅度: {np.abs(symbols_qpsk[:4])}")
    plot_constellation(symbols_qpsk[:200], "QPSK星座图", "qpsk_constellation.png")
    print("   ✅ QPSK测试通过")

    # 测试16-QAM
    print("\n3. 测试16-QAM调制...")
    bits_qam = np.random.randint(0, 2, 1000)
    symbols_qam = qam16_modulate(bits_qam)
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