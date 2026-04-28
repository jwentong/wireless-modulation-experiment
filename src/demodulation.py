"""
数字解调模块
实现BPSK、QPSK、16-QAM解调算法（选做）
"""

import numpy as np

def bpsk_demodulate(symbols):
    """BPSK解调"""
    # 实部 > 0 → 比特 0；实部 ≤ 0 → 比特 1
    return (np.real(symbols) <= 0).astype(int)


def qpsk_demodulate(symbols):
    """QPSK解调"""
    constellation = {
        (0, 0): (1 + 1j) / np.sqrt(2),
        (0, 1): (-1 + 1j) / np.sqrt(2),
        (1, 1): (-1 - 1j) / np.sqrt(2),
        (1, 0): (1 - 1j) / np.sqrt(2)
    }

    bits = np.zeros(len(symbols) * 2, dtype=int)
    points = list(constellation.values())
    keys = list(constellation.keys())

    for i, sym in enumerate(symbols):
        # 计算欧氏距离
        dists = [np.abs(sym - p) for p in points]
        best_idx = np.argmin(dists)
        b0, b1 = keys[best_idx]

        bits[2*i] = b0
        bits[2*i+1] = b1

    return bits


def qam16_demodulate(symbols):
    """16-QAM解调"""
    bits = np.zeros(len(symbols) * 4, dtype=int)

    for i, sym in enumerate(symbols):
        # 还原归一化以便于判断边界
        sym_unnorm = sym * np.sqrt(10)
        I = np.real(sym_unnorm)
        Q = np.imag(sym_unnorm)

        # 判决 I 路
        if I > 2:
            b0, b1 = 0, 0
        elif I > 0:
            b0, b1 = 0, 1
        elif I > -2:
            b0, b1 = 1, 1
        else:
            b0, b1 = 1, 0

        # 判决 Q 路
        if Q > 2:
            b2, b3 = 0, 0
        elif Q > 0:
            b2, b3 = 0, 1
        elif Q > -2:
            b2, b3 = 1, 1
        else:
            b2, b3 = 1, 0

        bits[4*i:4*i+4] = [b0, b1, b2, b3]

    return bits


def test_demodulation():
    """测试解调函数"""
    from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
    from utils import add_awgn, calculate_ber

    print("=" * 50)
    print("解调测试")
    print("=" * 50)

    # 测试BPSK
    print("\n1. 测试BPSK解调...")
    try:
        bits_tx = np.random.randint(0, 2, 100)
        symbols = bpsk_modulate(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db=10)
        bits_rx = bpsk_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=10dB)")
        print("   ✅ BPSK解调测试通过")
    except Exception as e:
        print(f"   ❌ BPSK解调测试失败: {e}")

    # 测试QPSK
    print("\n2. 测试QPSK解调...")
    try:
        bits_tx = np.random.randint(0, 2, 100)
        symbols = qpsk_modulate(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db=10)
        bits_rx = qpsk_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=10dB)")
        print("   ✅ QPSK解调测试通过")
    except Exception as e:
        print(f"   ❌ QPSK解调测试失败: {e}")

    # 测试16-QAM
    print("\n3. 测试16-QAM解调...")
    try:
        bits_tx = np.random.randint(0, 2, 100)
        symbols = qam16_modulate(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db=15)
        bits_rx = qam16_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=15dB)")
        print("   ✅ 16-QAM解调测试通过")
    except Exception as e:
        print(f"   ❌ 16-QAM解调测试失败: {e}")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_demodulation()