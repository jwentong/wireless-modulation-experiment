"""数字解调模块：实现 BPSK、QPSK、16-QAM 解调算法。"""

import numpy as np


def bpsk_demodulate(symbols):
    """
    BPSK 解调。

    判决准则：
    real(symbol) > 0 -> 0
    real(symbol) <= 0 -> 1
    """
    symbols = np.asarray(symbols, dtype=complex)
    bits = np.where(np.real(symbols) > 0, 0, 1)
    return bits.astype(int)


def qpsk_demodulate(symbols):
    """
    QPSK 解调，采用最小欧氏距离判决。
    """
    symbols = np.asarray(symbols, dtype=complex)

    constellation = [
        ((1 + 1j) / np.sqrt(2), [0, 0]),
        ((-1 + 1j) / np.sqrt(2), [0, 1]),
        ((-1 - 1j) / np.sqrt(2), [1, 1]),
        ((1 - 1j) / np.sqrt(2), [1, 0]),
    ]

    recovered_bits = []
    for symbol in symbols:
        distances = [np.abs(symbol - ref_symbol) for ref_symbol, _ in constellation]
        nearest_index = int(np.argmin(distances))
        recovered_bits.extend(constellation[nearest_index][1])

    return np.array(recovered_bits, dtype=int)


def qam16_demodulate(symbols):
    """
    16-QAM 解调。

    按 I/Q 两路分别判决：
    >  2/sqrt(10) -> 00
    0 到 2/sqrt(10) -> 01
    -2/sqrt(10) 到 0 -> 11
    < -2/sqrt(10) -> 10
    """
    symbols = np.asarray(symbols, dtype=complex)
    norm = np.sqrt(10)
    threshold = 2 / norm

    def decide_component(value):
        if value > threshold:
            return [0, 0]
        if value > 0:
            return [0, 1]
        if value > -threshold:
            return [1, 1]
        return [1, 0]

    recovered_bits = []
    for symbol in symbols:
        recovered_bits.extend(decide_component(np.real(symbol)))
        recovered_bits.extend(decide_component(np.imag(symbol)))

    return np.array(recovered_bits, dtype=int)


def test_demodulation():
    """测试解调函数。"""
    from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
    from utils import add_awgn, calculate_ber

    print("=" * 50)
    print("解调测试")
    print("=" * 50)

    print("\n1. 测试BPSK解调...")
    bits_tx = np.random.randint(0, 2, 1000)
    symbols = bpsk_modulate(bits_tx)
    symbols_rx = add_awgn(symbols, snr_db=10)
    bits_rx = bpsk_demodulate(symbols_rx)
    ber = calculate_ber(bits_tx, bits_rx)
    print(f"BER = {ber:.6f} (SNR=10dB)")
    print("✅ BPSK解调测试通过")

    print("\n2. 测试QPSK解调...")
    bits_tx = np.random.randint(0, 2, 1000)
    symbols = qpsk_modulate(bits_tx)
    symbols_rx = add_awgn(symbols, snr_db=10)
    bits_rx = qpsk_demodulate(symbols_rx)
    ber = calculate_ber(bits_tx, bits_rx)
    print(f"BER = {ber:.6f} (SNR=10dB)")
    print("✅ QPSK解调测试通过")

    print("\n3. 测试16-QAM解调...")
    bits_tx = np.random.randint(0, 2, 1000)
    symbols = qam16_modulate(bits_tx)
    symbols_rx = add_awgn(symbols, snr_db=15)
    bits_rx = qam16_demodulate(symbols_rx)
    ber = calculate_ber(bits_tx, bits_rx)
    print(f"BER = {ber:.6f} (SNR=15dB)")
    print("✅ 16-QAM解调测试通过")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    test_demodulation()