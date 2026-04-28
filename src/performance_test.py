import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
from demodulation import bpsk_demodulate, qpsk_demodulate, qam16_demodulate, calculate_ber

def simulate_ber(modulate_fn, demodulate_fn, snr_db_range, num_bits=10000):
    ber_list = []
    for snr_db in snr_db_range:
        bits = np.random.randint(0, 2, num_bits)
        symbols = modulate_fn(bits)
        # 添加AWGN噪声
        snr_linear = 10 ** (snr_db / 10)
        noise_std = 1 / np.sqrt(2 * snr_linear)
        noise = noise_std * (np.random.randn(*symbols.shape) + 1j * np.random.randn(*symbols.shape))
        rx_symbols = symbols + noise
        rx_bits = demodulate_fn(rx_symbols)
        ber = calculate_ber(bits[:len(rx_bits)], rx_bits)
        ber_list.append(max(ber, 1e-6))
    return ber_list

if __name__ == '__main__':
    snr_range = np.arange(0, 16, 1)
    os.makedirs('results', exist_ok=True)

    print("正在仿真BPSK...")
    ber_bpsk = simulate_ber(bpsk_modulate, bpsk_demodulate, snr_range)
    print("正在仿真QPSK...")
    bits_qpsk = lambda n: np.random.randint(0,2,n//2*2)
    ber_qpsk = simulate_ber(lambda b: qpsk_modulate(b), qpsk_demodulate, snr_range)
    print("正在仿真16-QAM...")
    ber_qam = simulate_ber(lambda b: qam16_modulate(b[:len(b)//4*4]), qam16_demodulate, snr_range)

    plt.figure(figsize=(8, 6))
    plt.semilogy(snr_range, ber_bpsk, 'b-o', label='BPSK')
    plt.semilogy(snr_range, ber_qpsk, 'r-s', label='QPSK')
    plt.semilogy(snr_range, ber_qam, 'g-^', label='16-QAM')
    plt.xlabel('SNR (dB)', fontsize=12)
    plt.ylabel('BER', fontsize=12)
    plt.title('BER vs SNR Performance', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, which='both', alpha=0.3)
    plt.savefig('results/ber_performance.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ BER曲线已保存到 results/ber_performance.png")
