"""
性能测试模块
测试调制解调系统在不同SNR下的BER性能（选做）
"""

import numpy as np
from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
from demodulation import bpsk_demodulate, qpsk_demodulate, qam16_demodulate
from utils import add_awgn, calculate_ber, generate_random_bits


def test_ber_performance(modulation_scheme='BPSK', num_bits=10000, snr_range=None):
    if snr_range is None:
        snr_range = np.arange(0, 16, 2)

    ber_values = []

    print(f"\n测试 {modulation_scheme} 性能...")
    print(f"比特数: {num_bits}, SNR范围: {snr_range[0]}~{snr_range[-1]} dB")
    print("-" * 40)

    if modulation_scheme == 'BPSK':
        modulate_func, demodulate_func = bpsk_modulate, bpsk_demodulate
    elif modulation_scheme == 'QPSK':
        modulate_func, demodulate_func = qpsk_modulate, qpsk_demodulate
    elif modulation_scheme == '16QAM':
        modulate_func, demodulate_func = qam16_modulate, qam16_demodulate
    else:
        raise ValueError(f"不支持的调制方式: {modulation_scheme}")

    for snr_db in snr_range:
        bits_tx = generate_random_bits(num_bits)
        symbols = modulate_func(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db)
        bits_rx = demodulate_func(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)

        ber_values.append(ber)
        print(f"SNR = {snr_db:2d} dB, BER = {ber:.6f}")

    return snr_range, np.array(ber_values)


def compare_modulations():
    print("=" * 50)
    print("数字调制性能对比测试")
    print("=" * 50)

    snr_range = np.arange(0, 16, 2)

    try:
        snr_bpsk, ber_bpsk = test_ber_performance('BPSK', num_bits=20000, snr_range=snr_range)
        snr_qpsk, ber_qpsk = test_ber_performance('QPSK', num_bits=20000, snr_range=snr_range)
        snr_qam, ber_qam = test_ber_performance('16QAM', num_bits=40000, snr_range=snr_range)

        import matplotlib.pyplot as plt
        import os
        from utils import setup_chinese_font

        setup_chinese_font()
        plt.figure(figsize=(10, 6))
        plt.semilogy(snr_bpsk, ber_bpsk, 'b-o', label='BPSK', linewidth=2)
        plt.semilogy(snr_qpsk, ber_qpsk, 'r-s', label='QPSK', linewidth=2)
        plt.semilogy(snr_qam, ber_qam, 'g-^', label='16-QAM', linewidth=2)

        plt.xlabel('SNR (dB)', fontsize=12)
        plt.ylabel('Bit Error Rate (BER)', fontsize=12)
        plt.title('数字调制方式性能对比', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, which='both', alpha=0.3)

        os.makedirs('results', exist_ok=True)
        filepath = os.path.join('results', 'ber_comparison.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"\n✅ 性能对比图已保存到: {filepath}")
        plt.close()

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")

    print("\n" + "=" * 50)

def main():
    compare_modulations()

if __name__ == "__main__":
    main()