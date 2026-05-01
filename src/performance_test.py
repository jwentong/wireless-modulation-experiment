"""性能测试模块：测试不同数字调制方式在 AWGN 信道下的 BER 性能。"""

import os

import matplotlib.pyplot as plt
import numpy as np

from demodulation import bpsk_demodulate, qpsk_demodulate, qam16_demodulate
from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
from utils import add_awgn, calculate_ber, generate_random_bits


def _valid_num_bits(modulation_scheme, num_bits):
    """保证随机比特数满足调制分组要求。"""
    if modulation_scheme == "BPSK":
        multiple = 1
    elif modulation_scheme == "QPSK":
        multiple = 2
    elif modulation_scheme == "16QAM":
        multiple = 4
    else:
        raise ValueError(f"不支持的调制方式: {modulation_scheme}")

    return (num_bits // multiple) * multiple


def test_ber_performance(modulation_scheme="BPSK", num_bits=10000, snr_range=None):
    """
    测试指定调制方式的 BER 性能。

    参数:
        modulation_scheme: 'BPSK', 'QPSK', 或 '16QAM'
        num_bits: 测试比特数量
        snr_range: SNR 范围，单位 dB

    返回:
        snr_range, ber_values
    """
    if snr_range is None:
        snr_range = np.arange(0, 16, 2)

    if modulation_scheme == "BPSK":
        modulate_func = bpsk_modulate
        demodulate_func = bpsk_demodulate
    elif modulation_scheme == "QPSK":
        modulate_func = qpsk_modulate
        demodulate_func = qpsk_demodulate
    elif modulation_scheme == "16QAM":
        modulate_func = qam16_modulate
        demodulate_func = qam16_demodulate
    else:
        raise ValueError(f"不支持的调制方式: {modulation_scheme}")

    num_bits = _valid_num_bits(modulation_scheme, num_bits)
    ber_values = []

    print(f"\n测试 {modulation_scheme} 性能...")
    print(f"比特数: {num_bits}, SNR范围: {snr_range[0]}~{snr_range[-1]} dB")
    print("-" * 40)

    for snr_db in snr_range:
        bits_tx = generate_random_bits(num_bits)
        symbols_tx = modulate_func(bits_tx)
        symbols_rx = add_awgn(symbols_tx, snr_db)
        bits_rx = demodulate_func(symbols_rx)

        ber = calculate_ber(bits_tx, bits_rx)
        ber_values.append(ber)

        print(f"SNR = {snr_db:2d} dB, BER = {ber:.8f}")

    return snr_range, np.array(ber_values)


def compare_modulations():
    """比较 BPSK、QPSK、16-QAM 的 BER 性能，并绘制曲线。"""
    print("=" * 50)
    print("数字调制性能对比测试")
    print("=" * 50)

    np.random.seed(42)
    snr_range = np.arange(0, 16, 1)

    snr_bpsk, ber_bpsk = test_ber_performance(
        "BPSK", num_bits=20000, snr_range=snr_range
    )
    snr_qpsk, ber_qpsk = test_ber_performance(
        "QPSK", num_bits=20000, snr_range=snr_range
    )
    snr_qam, ber_qam = test_ber_performance(
        "16QAM", num_bits=20000, snr_range=snr_range
    )

    os.makedirs("results", exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.semilogy(snr_bpsk, np.maximum(ber_bpsk, 1e-6), "o-", label="BPSK", linewidth=2)
    plt.semilogy(snr_qpsk, np.maximum(ber_qpsk, 1e-6), "s-", label="QPSK", linewidth=2)
    plt.semilogy(snr_qam, np.maximum(ber_qam, 1e-6), "^-", label="16-QAM", linewidth=2)

    plt.xlabel("SNR (dB)", fontsize=12)
    plt.ylabel("Bit Error Rate (BER)", fontsize=12)
    plt.title("数字调制方式 BER 性能对比", fontsize=14, fontweight="bold")
    plt.legend(fontsize=11)
    plt.grid(True, which="both", alpha=0.3)

    comparison_path = os.path.join("results", "ber_comparison.png")
    performance_path = os.path.join("results", "ber_performance.png")

    plt.savefig(comparison_path, dpi=300, bbox_inches="tight")
    plt.savefig(performance_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\n✅ BER对比图已保存到: {comparison_path}")
    print(f"✅ BER性能图已保存到: {performance_path}")
    print("=" * 50)

    return {
        "BPSK": (snr_bpsk, ber_bpsk),
        "QPSK": (snr_qpsk, ber_qpsk),
        "16QAM": (snr_qam, ber_qam),
    }


def main():
    """主函数。"""
    compare_modulations()


if __name__ == "__main__":
    main()